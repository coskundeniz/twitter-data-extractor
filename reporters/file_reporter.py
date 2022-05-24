from abc import ABC, abstractmethod
from typing import Any, Union

from utils import ExtractedDataType, logger


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
    def _save_user_data(self, extracted_data) -> None:
        """Save single user data"""

    @abstractmethod
    def _save_users_data(self, extracted_data) -> None:
        """Save users/friends/followers data"""

    @abstractmethod
    def _save_tweets_data(self, extracted_data) -> None:
        """Save tweets data"""
