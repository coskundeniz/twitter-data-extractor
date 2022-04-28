from argparse import ArgumentParser

from utils import logger, get_configuration


__author__ = "Coşkun Deniz <codenineeight@gmail.com>"


# def handle_exception(exp: YTViewsTrackerException) -> None:
#     """Print the error message and exit

#     :type exp: YTViewsTrackerException
#     :param exp: Exception raised by the views tracker components
#     """

#     logger.error(exp)
#     raise SystemExit() from exp


def get_arg_parser() -> ArgumentParser:
    """Get argument parser

    :rtype: ArgumentParser
    :returns: ArgumentParser object
    """

    arg_parser = ArgumentParser()
    arg_parser.add_argument("-u", "--user", help="Extract user data for the given handle")

    return arg_parser


def main(args) -> None:
    """Entry point for the tool

    :type args: Namespace
    :pram args: Command line args returned by ArgumentParser
    """

    pass


if __name__ == "__main__":

    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    try:
        main(args)

    except KeyboardInterrupt:
        logger.info("Program ended manually.")
