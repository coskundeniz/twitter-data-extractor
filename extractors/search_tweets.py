from typing import Generator

from extractors.tweets import TweetsExtractor
from models.tweet import Tweet
from twitter_api_service import TwitterAPIService
from utils import logger


Tweets = Generator[Tweet, None, None]


class SearchTweetsExtractor(TweetsExtractor):
    """Extract tweets for a search keyword

    :type cmdline_args: Namespace
    :param cmdline_args: Command line args returned by ArgumentParser
    """

    def __init__(self, cmdline_args: "Namespace") -> None:  # noqa: F821

        super().__init__(cmdline_args)

    def extract_data(self, api_service: TwitterAPIService) -> Tweets:
        """Extract tweets for a search keyword

        The recent search endpoint returns Tweets from the last seven days
        that match a search query.
        Tweet count can be limited with the --tweet_count(-tc) parameter.

        Retweets will be excluded.

        :type api_service: TwitterAPIService
        :param api_service: Twitter API client
        :rtype: Generator
        :returns: List of tweets data
        """

        logger.info(f"Getting tweets for keyword={self._search_keyword}")

        tweet_counter = 0

        for tweet_data in api_service.get_search_tweets(
            self._search_keyword,
            self._exclude,
            tweet_fields=self._tweet_fields,
            place_fields=self._place_fields,
            media_fields=self._media_fields,
            expansions=self._expansions,
            user_auth=self._is_authorized_user,
        ):

            tweet = Tweet(tweet_data)

            logger.debug(f"Search tweet data: {tweet}")

            tweet_counter += 1

            if self._tweet_count and tweet_counter > self._tweet_count:
                break

            yield tweet
