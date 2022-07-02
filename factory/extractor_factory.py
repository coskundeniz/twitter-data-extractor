from typing import Union

from extractors.base_extractor import BaseExtractor
from extractors.tweets import TweetsExtractor
from extractors.user import UserExtractor, UsersExtractor
from extractors.friends import FriendsExtractor
from extractors.followers import FollowersExtractor
from extractors.user_tweets import UserTweetsExtractor
from extractors.search_tweets import SearchTweetsExtractor
from exceptions import UnsupportedExtractorError


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

        if cmdline_args.user and not (
            cmdline_args.friends or cmdline_args.followers or cmdline_args.user_tweets
        ):
            extractor = UserExtractor(cmdline_args)
        elif cmdline_args.users:
            extractor = UsersExtractor(cmdline_args)
        elif cmdline_args.user and cmdline_args.friends:
            extractor = FriendsExtractor(cmdline_args)
        elif cmdline_args.user and cmdline_args.followers:
            extractor = FollowersExtractor(cmdline_args)
        elif cmdline_args.user and cmdline_args.user_tweets:
            extractor = UserTweetsExtractor(cmdline_args)
        elif cmdline_args.search:
            extractor = SearchTweetsExtractor(cmdline_args)
        else:
            raise UnsupportedExtractorError("Unsupported extractor! Check your parameters.")

        return extractor
