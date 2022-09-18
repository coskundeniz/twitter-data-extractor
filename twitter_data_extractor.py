from argparse import ArgumentParser

from exceptions import (
    TwitterAPISetupError,
    UnsupportedExtractorError,
    TwitterDataExtractorException,
    MissingUsernameParameterError,
    UserNotFoundError,
    PrivateAccountError,
    UnsupportedReporterError,
    ExtractorDatabaseError,
    MissingShareMailError,
)
from factory.extractor_factory import ExtractorFactory
from factory.reporter_factory import ReporterFactory
from twitter_api_service import TwitterAPIService
from utils import logger


__author__ = "Coşkun Deniz <codenineeight@gmail.com>"


def handle_exception(exp: TwitterDataExtractorException) -> None:
    """Print the error message and exit

    :type exp: TwitterDataExtractorException
    :param exp: Exception raised by the data extractor/reporter components
    """

    logger.error(exp)
    raise SystemExit() from exp


def get_arg_parser() -> ArgumentParser:
    """Get argument parser

    :rtype: ArgumentParser
    :returns: ArgumentParser object
    """

    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "-c", "--useconfig", action="store_true", help="Read configuration from config.json file"
    )
    arg_parser.add_argument(
        "-cf",
        "--configfile",
        default="config.json",
        help="Read configuration from given file",
    )
    arg_parser.add_argument(
        "--forme",
        action="store_true",
        help="Determine API user(account owner or on behalf of a user)",
    )
    arg_parser.add_argument("-u", "--user", help="Extract user data for the given username")
    arg_parser.add_argument(
        "-ul", "--users", help="Extract user data for the given comma separated usernames"
    )
    arg_parser.add_argument(
        "-fr", "--friends", action="store_true", help="Extract friends data for the given username"
    )
    arg_parser.add_argument(
        "-fl",
        "--followers",
        action="store_true",
        help="Extract followers data for the given username",
    )
    arg_parser.add_argument(
        "-ut",
        "--user_tweets",
        action="store_true",
        help="Extract tweets of user with the given username",
    )
    arg_parser.add_argument(
        "-s",
        "--search",
        help="Extract latest tweets for the given search keyword",
    )
    arg_parser.add_argument(
        "-tc",
        "--tweet_count",
        type=int,
        help="Limit the number of tweets gathered",
    )
    arg_parser.add_argument(
        "-e",
        "--excludes",
        default="retweets",
        help="Fields to exclude from tweets queried as comma separated values (replies,retweets)",
    )
    arg_parser.add_argument(
        "-ot",
        "--output_type",
        default="xlsx",
        help="Output file type (csv, xlsx, gsheets, mongodb or sqlite)",
    )
    arg_parser.add_argument("-of", "--output_file", default="results.xlsx", help="Output file name")
    arg_parser.add_argument(
        "-sm", "--share_mail", help="Mail address to share Google Sheets document"
    )

    return arg_parser


def main(args) -> None:
    """Entry point for the tool

    :type args: Namespace
    :pram args: Command line args returned by ArgumentParser
    """

    try:
        api_service = TwitterAPIService(args.forme)
        api_service.setup_api_access()

    except TwitterAPISetupError as exp:
        handle_exception(exp)

    try:
        extractor = ExtractorFactory.get_extractor(args)
    except UnsupportedExtractorError as exp:
        handle_exception(exp)

    try:
        extracted_data = extractor.extract_data(api_service)
    except (MissingUsernameParameterError, UserNotFoundError) as exp:
        handle_exception(exp)

    try:
        reporter = ReporterFactory.get_reporter(args)
    except (UnsupportedReporterError, ExtractorDatabaseError, MissingShareMailError) as exp:
        handle_exception(exp)

    try:
        reporter.save(extracted_data)
    except (PrivateAccountError, ExtractorDatabaseError) as exp:
        handle_exception(exp)


if __name__ == "__main__":

    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    try:
        main(args)

    except KeyboardInterrupt:
        logger.info("Program ended manually.")
