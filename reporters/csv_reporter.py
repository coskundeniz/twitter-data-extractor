import csv
from typing import Generator, Union

from models.user import User
from models.tweet import Tweet
from reporters.file_reporter import FileReporter
from utils import logger, ExtractedDataType


Friends = Generator[User, None, None]
Followers = Generator[User, None, None]
Tweets = Generator[Tweet, None, None]


class CsvReporter(FileReporter):
    """CSV report generator

    :type filename: str
    :param filename: Name of the output file
    :type extracted_data_type: ExtractedDataType
    :param extracted_data_type: Enum value for the extracted data type
    """

    def __init__(self, filename: str, extracted_data_type: ExtractedDataType) -> None:

        super().__init__(filename, extracted_data_type)

    def _save_user_data(self, extracted_data: User) -> None:
        """Save single user data

        :type extracted_data: User
        :param extracted_data: User object
        """

        logger.info("Saving user data...")

        logger.info(extracted_data)

        data = extracted_data.data

        with open(self._filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(self._user_data_header)
            writer.writerow(FileReporter._get_user_row_data(data))

    def _save_users_data(
        self, extracted_data: Union[list[User], Union[Friends, Followers]]
    ) -> None:
        """Save users/friends/followers data

        :type extracted_data: Generator
        :param extracted_data: List of Users(users/friends/followers)
        """

        is_friends_data = self._extracted_data_type == ExtractedDataType.FRIENDS

        if self._extracted_data_type == ExtractedDataType.USERS:
            logger.debug("Saving users data...")
        else:
            logger.debug(f"Saving {'friends' if is_friends_data else 'followers'} data...")

        with open(self._filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(self._user_data_header)

            for user_data_item in extracted_data:
                writer.writerow(CsvReporter._get_user_row_data(user_data_item.data))

    def _save_tweets_data(self, extracted_data: Tweets) -> None:
        """Save tweets data

        :type extracted_data: Generator
        :param extracted_data: List of Tweets
        """

        logger.debug("Saving tweets data...")

        if self._extracted_data_type == ExtractedDataType.USER_TWEETS:
            self._tweet_data_header.remove("Author")

        with open(self._filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(self._tweet_data_header)

            for tweet_data_item in extracted_data:
                writer.writerow(CsvReporter._get_tweet_row_data(tweet_data_item.data))
