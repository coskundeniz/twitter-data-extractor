class TwitterDataExtractorException(Exception):
    """Base exception for Twitter Data Extractor"""


class MissingUsernameParameterError(TwitterDataExtractorException):
    """Missing username for user extractor"""


class UserNotFoundError(TwitterDataExtractorException):
    """User with given handle could not be found"""


class UnsupportedExtractorError(TwitterDataExtractorException):
    """Unsupported extractor"""
