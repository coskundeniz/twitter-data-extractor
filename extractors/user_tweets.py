from typing import Generator

from exceptions import MissingUsernameParameterError
from extractors.tweets import TweetsExtractor
from models.tweet import Tweet
from twitter_api_service import TwitterAPIService
from utils import logger


Tweets = Generator[Tweet, None, None]


class UserTweets(TweetsExtractor):
    """Extract tweets of a user

    :type cmdline_args: Namespace
    :param cmdline_args: Command line args returned by ArgumentParser
    """

    def __init__(self, cmdline_args: "Namespace") -> None:  # noqa: F821

        super().__init__(cmdline_args)

    def extract_data(self, api_service: TwitterAPIService) -> Tweets:
        """Extract tweets of a user

        When "exclude=retweets" is used, the maximum historical Tweets returned
        is still 3200. When the "exclude=replies" parameter is used for any value,
        only the most recent 800 Tweets are available.
        Tweet count can be limited with the --tweet_count(-tc) parameter.

        Raises MissingUsernameParameter if username(-u) parameter
        is not passed as argument.

        :type api_service: TwitterAPIService
        :param api_service: Twitter API client
        :rtype: Generator
        :returns: List of tweets data
        """

        if not self._username:
            raise MissingUsernameParameterError("Username parameter is missing!")

        logger.info(f"Getting tweets for username={self._username}")

        tweet_counter = 0

        for tweet_data in api_service.get_user_tweets(
            self._username,
            tweet_fields=self._tweet_fields,
            place_fields=self._place_fields,
            media_fields=self._media_fields,
            expansions=self._expansions,
            exclude=self._exclude,
            user_auth=self._is_authorized_user,
        ):

            tweet = Tweet(tweet_data)

            logger.debug(f"User tweet data: {tweet}")

            tweet_counter += 1

            if self._tweet_count and tweet_counter > self._tweet_count:
                break

            yield tweet
