from abc import abstractmethod
from typing import Generator

from extractors.base_extractor import BaseExtractor
from models.tweet import Tweet
from twitter_api_service import TwitterAPIService


Tweets = Generator[Tweet, None, None]


class TweetsExtractor(BaseExtractor):
    """Extract tweets data

    :type cmdline_args: Namespace
    :param cmdline_args: Command line args returned by ArgumentParser
    """

    def __init__(self, cmdline_args: "Namespace") -> None:  # noqa: F821

        self._username = cmdline_args.user
        self._is_authorized_user = not cmdline_args.forme
        self._tweet_fields = [
            "attachments",
            "created_at",
            "entities",
            "geo",
            "lang",
            "public_metrics",
            "source",
        ]
        self._place_fields = ["country", "country_code", "geo", "place_type"]
        self._media_fields = ["url", "duration_ms", "width", "height", "public_metrics"]
        self._expansions = ["geo.place_id", "attachments.media_keys"]
        self._exclude = cmdline_args.excludes.split(",")

    @abstractmethod
    def extract_data(self, api_service: TwitterAPIService) -> Tweets:
        """Extract tweets data"""
