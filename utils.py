import json
import logging
from enum import Enum, auto
from logging.handlers import RotatingFileHandler

# from exceptions import UnsupportedConfigFileError


LOG_FILENAME = "tw_extractor.log"

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
    TWEETS = auto()


def get_configuration(filename: str = "config.json") -> dict:
    """Read configuration file

    :type filename: str
    :param filename: Name of the configuration file
    :rtype: dict
    :returns: Configuration as dict
    """

    # if not filename.endswith(".json"):
    #     raise UnsupportedConfigFileError("Config file must be a json file!")

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

    if args.user and not (args.friends or args.followers):
        result = ExtractedDataType.USER
    elif args.users:
        result = ExtractedDataType.USERS
    elif args.user and args.friends:
        result = ExtractedDataType.FRIENDS
    elif args.user and args.followers:
        result = ExtractedDataType.FOLLOWERS
    else:
        pass

    return result
