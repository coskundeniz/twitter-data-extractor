import json
import logging
from enum import Enum, auto
from logging.handlers import RotatingFileHandler
from typing import Optional

from exceptions import UnsupportedConfigFileError


LOG_FILENAME = "tw_data_extractor.log"

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = RotatingFileHandler(
    LOG_FILENAME, maxBytes=20971520, encoding="utf-8", backupCount=50
)
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
console_log_format = "%(asctime)s [%(levelname)5s] %(lineno)3d: %(message)s"
file_log_format = "%(asctime)s [%(levelname)5s] %(filename)s:%(lineno)3d: %(message)s"
console_formatter = logging.Formatter(console_log_format, datefmt="%d-%m-%Y %H:%M:%S")
console_handler.setFormatter(console_formatter)
file_formatter = logging.Formatter(file_log_format, datefmt="%d-%m-%Y %H:%M:%S")
file_handler.setFormatter(file_formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


class ExtractedDataType(Enum):
    USER = auto()
    USERS = auto()
    FRIENDS = auto()
    FOLLOWERS = auto()
    USER_TWEETS = auto()
    SEARCH_TWEETS = auto()


def get_configuration(filename: Optional[str] = "config.json") -> dict:
    """Read configuration file

    :type filename: str
    :param filename: Name of the configuration file
    :rtype: dict
    :returns: Configuration as dictionary
    """

    if not filename.endswith(".json"):
        raise UnsupportedConfigFileError("Config file must be a json file!")

    with open(filename, encoding="utf-8") as configfile:
        config = json.load(configfile)

    return config


def get_extracted_data_type(args: "Namespace") -> ExtractedDataType:
    """Determine extracted data type from arguments

    :type args: Namespace
    :pram args: Command line args returned by ArgumentParser
    :rtype: ExtractedDataType
    :returns: Enum value for the extracted data type
    """

    result = None

    config = get_configuration(args.configfile)

    if args.useconfig:
        is_user_extractor = config["user"] and not (
            args.friends or args.followers or args.user_tweets
        )
        is_users_extractor = config["users"] and not (
            args.friends or args.followers or args.user_tweets
        )
        is_friends_extractor = config["user"] and args.friends
        is_followers_extractor = config["user"] and args.followers
        is_user_tweets_extractor = config["user"] and args.user_tweets
        is_search_tweets_extractor = config["search"]
    else:
        is_user_extractor = args.user and not (args.friends or args.followers or args.user_tweets)
        is_users_extractor = args.users and not (args.friends or args.followers or args.user_tweets)
        is_friends_extractor = args.user and args.friends
        is_followers_extractor = args.user and args.followers
        is_user_tweets_extractor = args.user and args.user_tweets
        is_search_tweets_extractor = args.search

    if is_user_extractor:
        result = ExtractedDataType.USER
    elif is_users_extractor:
        result = ExtractedDataType.USERS
    elif is_friends_extractor:
        result = ExtractedDataType.FRIENDS
    elif is_followers_extractor:
        result = ExtractedDataType.FOLLOWERS
    elif is_user_tweets_extractor:
        result = ExtractedDataType.USER_TWEETS
    elif is_search_tweets_extractor:
        result = ExtractedDataType.SEARCH_TWEETS
    else:
        logger.error("Invalid extracted data type!")

    return result
