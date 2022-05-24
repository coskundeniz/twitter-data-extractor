from typing import Generator

from exceptions import PrivateAccountError
from extractors.user import UserExtractor
from twitter_api_service import TwitterAPIService
from models.user import User
from utils import logger


Followers = Generator[User, None, None]


class FollowersExtractor(UserExtractor):
    """Extract followers data of a user

    :type cmdline_args: Namespace
    :param cmdline_args: Command line args returned by ArgumentParser
    """

    def __init__(self, cmdline_args: "Namespace") -> None:  # noqa: F821

        super().__init__(cmdline_args)

    def extract_data(self, api_service: TwitterAPIService) -> Followers:
        """Extract all followers of the given user

        :type api_service: TwitterAPIService
        :param api_service: Twitter API client
        :rtype: Generator
        :returns: List of followers data
        """

        logger.info(f"Getting followers for username={self._username}")

        for follower_data in api_service.get_followers(
            self._username,
            user_fields=self._user_fields,
            expansions=self._expansions,
            user_auth=self._is_authorized_user,
        ):

            user_follower = User(follower_data)

            logger.debug(f"User follower data: {user_follower}")

            yield user_follower
