from exceptions import MissingUsernameParameterError, UserNotFoundError
from extractors.base_extractor import BaseExtractor
from models.user import User
from utils import logger
from twitter_api_service import TwitterAPIService


class UserExtractor(BaseExtractor):
    """Extract data for a single user

    :type cmdline_args: Namespace
    :param cmdline_args: Command line args returned by ArgumentParser
    """

    def __init__(self, cmdline_args: "Namespace") -> None:  # noqa: F821

        self._username = cmdline_args.user
        self._is_authorized_user = not cmdline_args.forme
        self._user_fields = [
            "created_at",
            "description",
            "entities",
            "location",
            "pinned_tweet_id",
            "profile_image_url",
            "protected",
            "public_metrics",
            "url",
            "verified",
        ]
        self._expansions = "pinned_tweet_id"

    def extract_data(self, api_service: TwitterAPIService) -> User:
        """Extract data for a single user

        Raises MissingUsernameParameter if username(-u) parameter
        is not passed as argument. Raises UserNotFoundError if API
        call returns None for the given username.

        :type api_service: TwitterAPIService
        :param api_service: Twitter API client
        :rtype: User
        :returns: Single user data
        """

        if not self._username:
            raise MissingUsernameParameterError("Username parameter is missing!")

        logger.info(f"Getting data for username={self._username}")

        user = api_service.get_user(
            username=self._username,
            user_fields=self._user_fields,
            expansions=self._expansions,
            user_auth=self._is_authorized_user,
        )

        if not user[0]:  # response.data
            raise UserNotFoundError(f"User with username={self._username} could not be found!")

        user_data = User(user)

        logger.debug(f"User data: {user_data}")

        return user_data
