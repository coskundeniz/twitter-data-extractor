from typing import Generator
from contextlib import contextmanager

import sqlite3

from exceptions import ExtractorDatabaseError
from models.user import User
from models.tweet import Tweet
from reporters.database_reporter import DatabaseReporter
from utils import ExtractedDataType, logger

Friends = Generator[User, None, None]
Followers = Generator[User, None, None]
Tweets = Generator[Tweet, None, None]
DBCursor = sqlite3.Connection.cursor


class SQLiteReporter(DatabaseReporter):
    """SQLite database

    Raises ExtractorDatabaseError if database connection
    is not established in 2 seconds.

    :type extracted_data_type: ExtractedDataType
    :param extracted_data_type: Enum value for the extracted data type
    """

    def __init__(self, extracted_data_type: ExtractedDataType) -> None:
        super().__init__(extracted_data_type)

        self._create_db_tables()

        # only used for logging
        self._filename = "SQLite Database: "

    def _save_user_data(self, extracted_data: User) -> None:
        """Save single user data

        :type extracted_data: User
        :param extracted_data: User object
        """

        logger.info("Saving user data...")

        self._filename += "users.db"

        logger.info(extracted_data)

        self._save_one_user(extracted_data)

    def _save_users_data(self, extracted_data: list[User]) -> None:
        """Save users/friends/followers data

        :type extracted_data: list
        :param extracted_data: List of Users(users/friends/followers)
        """

        self._filename += "users.db"

        is_friends_data = self._extracted_data_type == ExtractedDataType.FRIENDS

        if self._extracted_data_type == ExtractedDataType.USERS:
            logger.debug("Saving users data...")
        else:
            logger.debug(f"Saving {'friends' if is_friends_data else 'followers'} data...")

        for user_data_item in extracted_data:
            self._save_one_user(user_data_item)

    def _save_one_user(self, extracted_data: User) -> None:
        """Save one user to database

        Raises ExtractorDatabaseError if an error occurs
        during the save operation.

        :type extracted_data: User
        :param extracted_data: User object
        """

        try:
            with self._users_db() as users_db_cursor:
                user_id = extracted_data.data["id"]
                name = extracted_data.data["name"]
                username = extracted_data.data["username"]

                users_db_cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))

                found = users_db_cursor.fetchone()

                params = DatabaseReporter._get_user_row_data(extracted_data.data)

                if not found:
                    users_db_cursor.execute(
                        "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        params,
                    )
                    logger.info(f"User [{user_id}:{username}:{name}] added to database.")

                else:
                    logger.info(f"User [{user_id}:{username}:{name}] already exists. Updating...")

                    users_db_cursor.execute(
                        "REPLACE INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        params,
                    )

        except sqlite3.Error as exp:
            raise ExtractorDatabaseError(exp) from exp

    def _save_tweets_data(self, extracted_data: list[Tweet]) -> None:
        """Save tweets data

        Use user_tweets table if extracted data type is user tweets,
        search_tweets table otherwise.

        Raises ExtractorDatabaseError if an error occurs
        during the save operation.

        :type extracted_data: list
        :param extracted_data: List of Tweets
        """

        logger.debug("Saving tweets data...")

        if self._extracted_data_type == ExtractedDataType.USER_TWEETS:
            tweets_db = self._user_tweets_db
            self._filename += "user_tweets.db"
            table = "user_tweets"
        elif self._extracted_data_type == ExtractedDataType.SEARCH_TWEETS:
            tweets_db = self._search_tweets_db
            self._filename += "search_tweets.db"
            table = "search_tweets"

        try:
            with tweets_db() as tweets_db_cursor:
                for tweet_data_item in extracted_data:
                    tweet_id = tweet_data_item.data["id"]

                    tweets_db_cursor.execute(
                        f"SELECT tweet_id FROM {table} WHERE tweet_id=?", (tweet_id,)
                    )

                    found = tweets_db_cursor.fetchone()

                    params = DatabaseReporter._get_tweet_row_data(tweet_data_item.data)

                    if not found:
                        if table == "user_tweets":
                            tweets_db_cursor.execute(
                                f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                params,
                            )
                        else:
                            # there is one more field(author) for search tweets
                            tweets_db_cursor.execute(
                                f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                params,
                            )

                        logger.info(f"Tweet[{tweet_id}] added to database.")

                    else:
                        logger.info(f"Tweet[{tweet_id}] already exists. Updating...")

                        if table == "user_tweets":
                            tweets_db_cursor.execute(
                                f"REPLACE INTO {table} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                params,
                            )
                        else:
                            tweets_db_cursor.execute(
                                f"REPLACE INTO {table} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                params,
                            )

        except sqlite3.Error as exp:
            raise ExtractorDatabaseError(exp) from exp

    def _create_db_tables(self) -> None:
        """Create tables for users, user tweets and search tweets databases"""

        with self._users_db() as users_db_cursor:
            users_db_cursor.execute(
                """CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY NOT NULL,
                    username TEXT NOT NULL,
                    name TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    description TEXT NOT NULL,
                    url_items TEXT,
                    hashtag_items TEXT,
                    mention_items TEXT,
                    location TEXT,
                    pinned_tweet_id TEXT,
                    pinned_tweet_text TEXT,
                    profile_image_url TEXT,
                    protected TEXT NOT NULL,
                    public_metrics TEXT NOT NULL,
                    url TEXT,
                    verified TEXT NOT NULL
                );"""
            )

        with self._user_tweets_db() as user_tweets_db_cursor:
            user_tweets_db_cursor.execute(
                """CREATE TABLE IF NOT EXISTS user_tweets (
                    tweet_id TEXT PRIMARY KEY NOT NULL,
                    text TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    source TEXT NOT NULL,
                    language TEXT NOT NULL,
                    public_metrics TEXT NOT NULL,
                    urls TEXT,
                    hashtags TEXT,
                    mentions TEXT,
                    media TEXT,
                    places TEXT
                );"""
            )

        with self._search_tweets_db() as search_tweets_db_cursor:
            search_tweets_db_cursor.execute(
                """CREATE TABLE IF NOT EXISTS search_tweets (
                    tweet_id TEXT PRIMARY KEY NOT NULL,
                    text TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    source TEXT NOT NULL,
                    language TEXT NOT NULL,
                    public_metrics TEXT NOT NULL,
                    urls TEXT,
                    hashtags TEXT,
                    mentions TEXT,
                    media TEXT,
                    places TEXT,
                    author TEXT
                );"""
            )

    @contextmanager
    def _users_db(self) -> DBCursor:
        """Context manager that returns users db cursor

        :rtype: sqlite3.Connection.cursor
        :returns: Database connection cursor
        """

        try:
            users_db = sqlite3.connect("users.db")
            yield users_db.cursor()

        except sqlite3.Error as exp:
            print(exp)
            raise ExtractorDatabaseError("Failed to connect to users database!") from exp

        finally:
            users_db.commit()
            users_db.close()

    @contextmanager
    def _user_tweets_db(self) -> DBCursor:
        """Context manager that returns user_tweets db cursor

        :rtype: sqlite3.Connection.cursor
        :returns: Database connection cursor
        """

        try:
            user_tweets_db = sqlite3.connect("user_tweets.db")
            yield user_tweets_db.cursor()

        except sqlite3.Error as exp:
            raise ExtractorDatabaseError("Failed to connect to user_tweets database!") from exp

        finally:
            user_tweets_db.commit()
            user_tweets_db.close()

    @contextmanager
    def _search_tweets_db(self) -> DBCursor:
        """Context manager that returns search_tweets db cursor

        :rtype: sqlite3.Connection.cursor
        :returns: Database connection cursor
        """

        try:
            search_tweets_db = sqlite3.connect("search_tweets.db")
            yield search_tweets_db.cursor()

        except sqlite3.Error as exp:
            raise ExtractorDatabaseError("Failed to connect to search_tweets database!") from exp

        finally:
            search_tweets_db.commit()
            search_tweets_db.close()
