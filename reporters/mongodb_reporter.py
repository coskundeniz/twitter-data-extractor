from typing import Generator

from pymongo import MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError

from exceptions import ExtractorDatabaseError
from models.user import User
from models.tweet import Tweet
from reporters.database_reporter import DatabaseReporter
from utils import ExtractedDataType, logger

Friends = Generator[User, None, None]
Followers = Generator[User, None, None]
Tweets = Generator[Tweet, None, None]


class MongoDBReporter(DatabaseReporter):
    """MongoDB database reporter

    Raises ExtractorDatabaseError if database connection
    is not established in 2 seconds.

    :type extracted_data_type: ExtractedDataType
    :param extracted_data_type: Enum value for the extracted data type
    """

    DB_NAME = "tw_data_extractor_db"
    DB_ADDR = "0.0.0.0"
    DB_PORT = 27017

    def __init__(self, extracted_data_type: ExtractedDataType) -> None:

        super().__init__(extracted_data_type)

        try:
            self.db_client = MongoClient(self.DB_ADDR, self.DB_PORT, serverSelectionTimeoutMS=2000)
            self.db_client.server_info()

        except ServerSelectionTimeoutError as exp:
            raise ExtractorDatabaseError(
                "Failed to connect to database! Please check if database server is running."
            ) from exp

        self.db = self.db_client[self.DB_NAME]
        self.users_db = self.db["users"]

        if self._extracted_data_type == ExtractedDataType.USER_TWEETS:
            self.tweets_db = self.db["user_tweets"]
        elif self._extracted_data_type == ExtractedDataType.SEARCH_TWEETS:
            self.tweets_db = self.db["search_tweets"]

        # only used for logging
        self._filename = f"MongoDB Database: {self.DB_NAME}"

    def _save_user_data(self, extracted_data: User) -> None:
        """Save single user data

        :type extracted_data: User
        :param extracted_data: User object
        """

        logger.info("Saving user data...")

        self._filename += ", MongoDB Collection: users"

        logger.info(extracted_data)

        self._save_one_user(extracted_data)

    def _save_users_data(self, extracted_data: list[User]) -> None:
        """Save users/friends/followers data

        :type extracted_data: list
        :param extracted_data: List of Users(users/friends/followers)
        """

        self._filename += ", MongoDB Collection: users"

        is_friends_data = self._extracted_data_type == ExtractedDataType.FRIENDS

        if self._extracted_data_type == ExtractedDataType.USERS:
            logger.debug("Saving users data...")
        else:
            logger.debug(f"Saving {'friends' if is_friends_data else 'followers'} data...")

        for user_data_item in extracted_data:
            self._save_one_user(user_data_item)

    def _save_one_user(self, extracted_data) -> None:
        """Save one user to database

        Raises ExtractorDatabaseError if an error occurs
        during the save operation.

        :type extracted_data: User
        :param extracted_data: User object
        """

        try:
            if not self.users_db.find_one({"id": extracted_data.data["id"]}):
                self.users_db.insert_one(extracted_data.data)

            else:
                user_id = extracted_data.data["id"]
                name = extracted_data.data["name"]
                username = extracted_data.data["username"]
                logger.info(f"User [{user_id}:{username}:{name}] already exists. Updating...")

                self.users_db.replace_one({"id": user_id}, extracted_data.data)

        except PyMongoError as exp:
            raise ExtractorDatabaseError(exp) from exp

    def _save_tweets_data(self, extracted_data: list[Tweet]) -> None:
        """Save tweets data

        Use user_tweets collection if extracted data type is user tweets,
        search_tweets collection otherwise.

        :type extracted_data: list
        :param extracted_data: List of Tweets
        """

        logger.debug("Saving tweets data...")

        if self._extracted_data_type == ExtractedDataType.USER_TWEETS:
            self._filename += ", MongoDB Collection: user_tweets"
        else:
            self._filename += ", MongoDB Collection: search_tweets"

        for tweet_data_item in extracted_data:

            try:
                if not self.tweets_db.find_one({"id": tweet_data_item.data["id"]}):
                    self.tweets_db.insert_one(tweet_data_item.data)

                else:
                    tweet_id = tweet_data_item.data["id"]
                    logger.info(f"Tweet [{tweet_id}] already exists. Updating...")

                    self.tweets_db.replace_one({"id": tweet_id}, tweet_data_item.data)

            except PyMongoError as exp:
                raise ExtractorDatabaseError(exp) from exp
