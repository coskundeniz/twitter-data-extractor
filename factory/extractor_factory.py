from extractors import base_extractor
from extractors.user import UserExtractor, UsersExtractor
from extractors.friends import FriendsExtractor
from extractors.followers import FollowersExtractor
from exceptions import UnsupportedExtractorError


class ExtractorFactory:
    """Factory class for data extractors"""

    @staticmethod
    def get_extractor(cmdline_args: "Namespace") -> base_extractor.BaseExtractor:  # noqa: F821
        """Get specific data extractor according to arguments

        Raises UnsupportedExtractorError if an extractor cannot be found
        for the given parameters.

        :type cmdline_args: Namespace
        :param cmdline_args: Command line args returned by ArgumentParser
        :rtype: base_extractor.BaseExtractor
        :returns: Concrete BaseExtractor object
        """

        extractor = None

        # if (cmdline_args.user and
        # not (cmdline_args.friends or cmdline_args.followers or cmdline_args.ff)):
        if cmdline_args.user and not (cmdline_args.friends or cmdline_args.followers):
            extractor = UserExtractor(cmdline_args)
        elif cmdline_args.users:
            extractor = UsersExtractor(cmdline_args)
        elif cmdline_args.user and cmdline_args.friends:
            extractor = FriendsExtractor(cmdline_args)
        elif cmdline_args.user and cmdline_args.followers:
            extractor = FollowersExtractor(cmdline_args)
        else:
            raise UnsupportedExtractorError("Unsupported extractor! Check your parameters.")

        return extractor
