from typing import Generator, Union

from models.user import User
from models.tweet import Tweet
from reporters.reporter import Reporter
from utils import ExtractedDataType

Friends = Generator[User, None, None]
Followers = Generator[User, None, None]
Tweets = Generator[Tweet, None, None]


class FileReporter(Reporter):
    """Base class for csv, excel, and gsheets reporters"""

    def __init__(self, filename: str, extracted_data_type: ExtractedDataType) -> None:

        super().__init__(extracted_data_type)

        self._filename = filename

    def _save_user_data(self, extracted_data: User) -> None:
        """Save single user data"""

    def _save_users_data(self, extracted_data: Union[list[User], Union[Friends, Friends]]) -> None:
        """Save users/friends/followers data"""

    def _save_tweets_data(self, extracted_data: Tweets) -> None:
        """Save tweets data"""
