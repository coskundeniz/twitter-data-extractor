from argparse import ArgumentParser

from exceptions import (
    UnsupportedExtractorError,
    TwitterDataExtractorException,
    MissingUsernameParameterError,
    UserNotFoundError,
)
from factory.extractor_factory import ExtractorFactory
from twitter_api_service import TwitterAPIService
from utils import logger, get_configuration


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
        "--forme",
        action="store_true",
        help="Determine API user(accounut owner or on behalf of a user)",
    )
    arg_parser.add_argument("-u", "--user", help="Extract user data for the given username")
    arg_parser.add_argument(
        "-fr", "--friends", action="store_true", help="Extract friends data for the given username"
    )

    return arg_parser


def main(args) -> None:
    """Entry point for the tool

    :type args: Namespace
    :pram args: Command line args returned by ArgumentParser
    """

    api_service = TwitterAPIService(args.forme)
    api_service.setup_api_access()

    try:
        extractor = ExtractorFactory.get_extractor(args)
    except UnsupportedExtractorError as exp:
        handle_exception(exp)

    try:
        extracted_data = extractor.extract_data(api_service)
    except (MissingUsernameParameterError, UserNotFoundError) as exp:
        handle_exception(exp)

    # print(extracted_data)

    for friend in extracted_data:
        print(friend)


if __name__ == "__main__":

    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    try:
        main(args)

    except KeyboardInterrupt:
        logger.info("Program ended manually.")
