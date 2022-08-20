from abc import abstractmethod
from typing import Generator

from extractors.base_extractor import BaseExtractor
from models.tweet import Tweet
from twitter_api_service import TwitterAPIService
from utils import get_configuration


Tweets = Generator[Tweet, None, None]


class TweetsExtractor(BaseExtractor):
    """Extract tweets data

    :type cmdline_args: Namespace
    :param cmdline_args: Command line args returned by ArgumentParser
    """

    def __init__(self, cmdline_args: "Namespace") -> None:  # noqa: F821

        config = get_configuration(cmdline_args.configfile)

        if cmdline_args.useconfig and config["user"]:
            self._username = config["user"]
        elif not cmdline_args.useconfig and cmdline_args.user:
            self._username = cmdline_args.user
        else:
            self._username = None

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
        self._exclude = (
            config["excludes"].split(",")
            if cmdline_args.useconfig
            else cmdline_args.excludes.split(",")
        )

        if cmdline_args.useconfig and config["search"]:
            self._search_keyword = config["search"]
        elif not cmdline_args.useconfig and cmdline_args.search:
            self._search_keyword = cmdline_args.search
        else:
            self._search_keyword = None

        if cmdline_args.useconfig and config["tweet_count"]:
            self._tweet_count = config["tweet_count"]
        elif not cmdline_args.useconfig and cmdline_args.tweet_count:
            self._tweet_count = cmdline_args.tweet_count
        else:
            self._tweet_count = 20

    @abstractmethod
    def extract_data(self, api_service: TwitterAPIService) -> Tweets:
        """Extract tweets data"""
