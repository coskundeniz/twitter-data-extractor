from typing import Union

from extractors.base_extractor import BaseExtractor
from extractors.tweets import TweetsExtractor
from extractors.user import UserExtractor, Users
from extractors.friends import Friends
from extractors.followers import Followers
from extractors.user_tweets import UserTweets
from extractors.search_tweets import SearchTweets
from exceptions import UnsupportedExtractorError
from utils import get_configuration


class ExtractorFactory:
    """Factory class for data extractors"""

    @staticmethod
    def get_extractor(
        cmdline_args: "Namespace",  # noqa: F821
    ) -> Union[BaseExtractor, TweetsExtractor]:
        """Get specific data extractor according to arguments

        Raises UnsupportedExtractorError if an extractor cannot be found
        for the given parameters.

        :type cmdline_args: Namespace
        :param cmdline_args: Command line args returned by ArgumentParser
        :rtype: BaseExtractor or TweetsExtractor
        :returns: Concrete BaseExtractor or TweetsExtractor object
        """

        extractor = None

        config = get_configuration(cmdline_args.configfile)

        if cmdline_args.useconfig:
            is_user_extractor = config["user"] and not (
                cmdline_args.friends or cmdline_args.followers or cmdline_args.user_tweets
            )
            is_users_extractor = config["users"] and not (
                cmdline_args.friends or cmdline_args.followers or cmdline_args.user_tweets
            )
            is_friends_extractor = config["user"] and cmdline_args.friends
            is_followers_extractor = config["user"] and cmdline_args.followers
            is_user_tweets_extractor = config["user"] and cmdline_args.user_tweets
            is_search_tweets_extractor = config["search"]
        else:
            is_user_extractor = cmdline_args.user and not (
                cmdline_args.friends or cmdline_args.followers or cmdline_args.user_tweets
            )
            is_users_extractor = cmdline_args.users and not (
                cmdline_args.friends or cmdline_args.followers or cmdline_args.user_tweets
            )
            is_friends_extractor = cmdline_args.user and cmdline_args.friends
            is_followers_extractor = cmdline_args.user and cmdline_args.followers
            is_user_tweets_extractor = cmdline_args.user and cmdline_args.user_tweets
            is_search_tweets_extractor = cmdline_args.search

        if is_user_extractor:
            extractor = UserExtractor(cmdline_args)
        elif is_users_extractor:
            extractor = Users(cmdline_args)
        elif is_friends_extractor:
            extractor = Friends(cmdline_args)
        elif is_followers_extractor:
            extractor = Followers(cmdline_args)
        elif is_user_tweets_extractor:
            extractor = UserTweets(cmdline_args)
        elif is_search_tweets_extractor:
            extractor = SearchTweets(cmdline_args)
        else:
            raise UnsupportedExtractorError("Unsupported extractor! Check your parameters.")

        return extractor
