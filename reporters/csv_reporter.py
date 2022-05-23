import csv

from models.user import User
from models.tweet import Tweet
from reporters.file_reporter import FileReporter
from utils import logger, ExtractedDataType


class CsvReporter(FileReporter):
    """CSV report generator

    :type filename: str
    :param filename: Name of the output file
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
            writer.writerow(CsvReporter._get_user_row_data(data))

    def _save_users_data(self, extracted_data: list[User]) -> None:
        """Save friends/followers data

        :type extracted_data: list
        :param extracted_data: List of Users(friends/followers)
        """

        is_friends_data = self._extracted_data_type == ExtractedDataType.FRIENDS

        logger.debug(f"Saving {'friends' if is_friends_data else 'followers'} data...")

        with open(self._filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(self._user_data_header)

            for user_data_item in extracted_data:
                writer.writerow(CsvReporter._get_user_row_data(user_data_item.data))

    def _save_tweets_data(self, extracted_data: list[Tweet]) -> None:
        """Save tweets data

        :type extracted_data: list
        :param extracted_data: List of Tweets
        """

        pass

    @staticmethod
    def _get_user_row_data(data: dict) -> list:
        """Get user data for the row

        :type data: dict
        :param data: Data dictionary for the User
        """

        return [
            data["id"],
            data["username"],
            data["name"],
            data["created_at"],
            data["description"],
            " ".join(url for url in data["entities"]["url_items"]),
            " ".join(hashtag for hashtag in data["entities"]["hashtag_items"]),
            " ".join(mention for mention in data["entities"]["mention_items"]),
            data["location"],
            data["pinned_tweet_id"],
            data["pinned_tweet_text"],
            data["profile_image_url"],
            data["protected"],
            data["public_metrics"],
            data["url"],
            data["verified"],
        ]
