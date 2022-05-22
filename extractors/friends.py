from typing import Generator

from exceptions import PrivateAccountError
from extractors.user import UserExtractor
from twitter_api_service import TwitterAPIService
from models.user import User
from utils import logger


Friends = Generator[User, None, None]


class FriendsExtractor(UserExtractor):
    """Extract friends data of a user

    :type cmdline_args: Namespace
    :param cmdline_args: Command line args returned by ArgumentParser
    """

    def __init__(self, cmdline_args: "Namespace") -> None:  # noqa: F821

        super().__init__(cmdline_args)

    def extract_data(self, api_service: TwitterAPIService) -> Friends:
        """Extract all friends of the given user

        Raises MissingUsernameParameter if username(-u) parameter
        is not passed as argument. Raises UserNotFoundError if API
        call returns None for the given username.

        :type api_service: TwitterAPIService
        :param api_service: Twitter API client
        :rtype: Generator
        :returns: List of friends data
        """

        logger.info(f"Getting friends for username={self._username}")

        for friend_data in api_service.get_friends(
            self._username,
            user_fields=self._user_fields,
            expansions=self._expansions,
            user_auth=self._is_authorized_user,
        ):

            user_friend = User(friend_data)

            logger.debug(f"User friend data: {user_friend}")

            yield user_friend
