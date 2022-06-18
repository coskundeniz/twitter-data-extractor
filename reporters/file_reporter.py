from abc import ABC, abstractmethod
from typing import Any, Generator, Union

from openpyxl.utils.datetime import to_ISO8601

from models.user import User
from models.tweet import Tweet
from utils import ExtractedDataType, logger

Friends = Generator[User, None, None]
Followers = Generator[User, None, None]
Tweets = Generator[Tweet, None, None]


class FileReporter(ABC):
    """Base class for csv, excel, and gsheets reporters"""

    def __init__(self, filename: str, extracted_data_type: ExtractedDataType) -> None:

        self._filename = filename
        self._extracted_data_type = extracted_data_type
        self._user_data_header = [
            "ID",
            "Username",
            "Name",
            "Created At",
            "Bio",
            "URLs",
            "Hashtags",
            "Mentions",
            "Location",
            "Pinned Tweet ID",
            "Pinned Tweet",
            "Profile Image URL",
            "Account Protected",
            "Public Metrics",
            "Url",
            "Verified",
        ]
        self._tweet_data_header = [
            "ID",
            "Text",
            "Created At",
            "Source",
            "Language",
            "Public Metrics",
            "URLs",
            "Hashtags",
            "Mentions",
            "Media",
            "Place",
        ]

    def save(self, extracted_data: Union[Any, list[Any]]) -> None:
        """Save extracted data on the output file

        :type extracted_data: Union[Any, list[Any]]
        :param extracted_data: Data consist of single User object, multiple User or Tweet objects
        """

        logger.debug(f"Saving data to {self._filename}")

        if self._extracted_data_type == ExtractedDataType.USER:
            self._save_user_data(extracted_data)
        elif (
            self._extracted_data_type == ExtractedDataType.USERS
            or self._extracted_data_type == ExtractedDataType.FRIENDS
            or self._extracted_data_type == ExtractedDataType.FOLLOWERS
        ):
            self._save_users_data(extracted_data)
        else:
            self._save_tweets_data(extracted_data)

        logger.info(f"Data saved to {self._filename}")

    @abstractmethod
    def _save_user_data(self, extracted_data: User) -> None:
        """Save single user data"""

    @abstractmethod
    def _save_users_data(self, extracted_data: Union[list[User], Union[Friends, Friends]]) -> None:
        """Save users/friends/followers data"""

    @abstractmethod
    def _save_tweets_data(self, extracted_data: Tweets) -> None:
        """Save tweets data"""

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
            to_ISO8601(data["created_at"]),
            data["description"],
            " ".join(url for url in data["entities"]["url_items"]),
            " ".join(hashtag for hashtag in data["entities"]["hashtag_items"]),
            " ".join(mention for mention in data["entities"]["mention_items"]),
            data["location"],
            data["pinned_tweet_id"],
            data["pinned_tweet_text"],
            data["profile_image_url"],
            data["protected"],
            " | ".join(f"{k}: {v}" for k, v in data["public_metrics"].items()),
            data["url"],
            data["verified"],
        ]

    @staticmethod
    def _get_tweet_row_data(data: dict) -> list:
        """Get tweet data for the row

        :type data: dict
        :param data: Data dictionary for the Tweet
        """

        def _prepare_media_output():

            media_data = ""
            for media in data["media"]:
                media_data += f"Key: {media['media_key']}, Type: {media['type']}\n"
                media_data += f"URL: {media['url']}\n"
                media_data += f"Width: {media['width']}, Height: {media['width']}"

                if media["type"] == "video":
                    media_data += f"Duration: {media['duration_ms']}\n"
                    media_data += f"View count: {media['public_metrics']['view_count']}\n"

                if len(data["media"]) > 1:
                    media_data += "\n-------\n"

            return media_data

        def _prepare_place_output():

            place_data = ""

            for place in data["places"]:
                place_data += f"ID: {place['id']}\nFull name: {place['full_name']}\n"
                place_data += f"Country: {place['country']} ({place['country_code']})\n"
                place_data += f"Type: {place['place_type']}\n"
                place_data += f"Coords: {place['geo']['bbox']}"

                if len(data["places"]) > 1:
                    place_data += "\n-------\n"

            return place_data

        return [
            data["id"],
            data["text"],
            to_ISO8601(data["created_at"]),
            data["source"],
            data["language"],
            " | ".join(f"{k}: {v}" for k, v in data["public_metrics"].items()),
            " ".join(url for url in data["entities"]["url_items"]),
            " ".join(hashtag for hashtag in data["entities"]["hashtag_items"]),
            " ".join(mention for mention in data["entities"]["mention_items"]),
            _prepare_media_output(),
            _prepare_place_output(),
        ]
