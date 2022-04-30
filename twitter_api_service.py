import os
import json

import tweepy

from utils import logger


class TwitterAPIService:
    """Handle API requests

    :type forme: bool
    :param forme: Whether the API will be used for account owner or authorized user
    """

    def __init__(self, forme: bool = False) -> None:

        self._forme = forme
        self._api_v1 = None
        self._api_v2 = None
        self._authorized_client = None
        self._current_client = None
        self._external_user_creds_file = "external_user_creds.json"

    def setup_api_access(self) -> None:
        """Setup access for developer or authorized user"""

        if self._forme:
            self._setup_api_access_v2()
            self._current_client = self._api_v2
        else:
            self._authorize_with_pin()
            self._current_client = self._authorized_client

    def get_user(
        self,
        username: str,
        user_fields: list[str] = None,
        expansions: str = None,
        user_auth: bool = False,
    ) -> tuple:
        """Get user given by username

        Pass user fields, tweet fields, and expansions for additional data.

        https://docs.tweepy.org/en/latest/client.html#user-fields
        https://docs.tweepy.org/en/latest/client.html#expansions

        :type username: str
        :param username: Twitter username
        :type user_fields: list
        :param user_fields: Additional user fields to get
        :type expansions: list
        :param expansions: Additional data objects to get
        :rtype: tuple
        :returns: Response data and includes objects as tuple
        """

        response = self._current_client.get_user(
            username=username,
            user_fields=user_fields,
            expansions=expansions,
            user_auth=user_auth,
        )

        return (response.data, response.includes)

    def _setup_api_access_v1(self) -> None:
        """Setup access for Twitter v1 API"""

        logger.debug("Setting up v1 API access...")

        try:
            ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
            ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
            CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
            CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
        except KeyError:
            logger.error("Failed to find credentials setup! Setup environment variables.")

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        self._api_v1 = tweepy.API(auth, wait_on_rate_limit=True)

    def _setup_api_access_v2(self) -> None:
        """Setup access for Twitter v2 API as app"""

        logger.debug("Setting up v2 API access...")

        try:
            BEARER_TOKEN = os.environ["TWITTER_BEARER_TOKEN_CODE"]
        except KeyError:
            logger.error("Failed to find credentials setup! Setup environment variables.")

        self._api_v2 = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

    def _authorize_with_pin(self) -> None:
        """Authorize user using the PIN authentication"""

        logger.debug("Setting up v2 API access for authorized user...")

        try:
            CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY_CODE"]
            CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET_CODE"]
        except KeyError:
            logger.error("Failed to find credentials setup! Setup environment variables.")

        oauth1_user_handler = tweepy.OAuth1UserHandler(
            CONSUMER_KEY, CONSUMER_SECRET, callback="oob"
        )

        if not self._is_credentials_exists():
            print("\nPlease get the PIN from the following URL\n")

            print(oauth1_user_handler.get_authorization_url())

            verifier = input("\nEnter PIN: ")

            access_token, access_token_secret = oauth1_user_handler.get_access_token(verifier)

            self._save_on_behalf_user_credentials(access_token, access_token_secret)
        else:
            access_token, access_token_secret = self._get_external_user_credentials()

        self._authorized_client = tweepy.Client(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True,
        )

        logger.info(
            f"Performing operations on behalf of {self._authorized_client.get_me().data.username}"
        )

    def _save_on_behalf_user_credentials(self, access_token: str, access_token_secret: str) -> None:
        """Save access credentials for the on behalf user

        :type access_token: str
        :param access_token: Authorized user access token
        :type access_token_secret: str
        :param access_token_secret: Authorized user access token secret
        """

        data = {"access_token": access_token, "access_token_secret": access_token_secret}

        with open(self._external_user_creds_file, "w") as creds_file:
            json.dump(data, creds_file)

    def _get_external_user_credentials(self) -> tuple[str, str]:
        """Read access credentials from file for authorized account

        :rtype: tuple
        :returns: Access token and access token secret pair
        """

        logger.debug("Reading credentials from file...")

        with open(self._external_user_creds_file) as creds_file:
            creds_data = json.load(creds_file)

        return (creds_data["access_token"], creds_data["access_token_secret"])

    def _is_credentials_exists(self) -> bool:
        """Check if the credentials file exists

        :rtype: bool
        :returns: Whether credentials file exists
        """

        return os.path.exists(self._external_user_creds_file)