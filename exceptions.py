class TwitterDataExtractorException(Exception):
    """Base exception for Twitter Data Extractor"""


class MissingUsernameParameterError(TwitterDataExtractorException):
    """Missing username for user extractor"""


class UserNotFoundError(TwitterDataExtractorException):
    """User with given handle could not be found"""


class UnsupportedExtractorError(TwitterDataExtractorException):
    """Unsupported extractor"""


class PrivateAccountError(TwitterDataExtractorException):
    """Private account error"""


class UnsupportedConfigFileError(TwitterDataExtractorException):
    """Unsupported config file error"""


class UnsupportedReporterError(TwitterDataExtractorException):
    """Unsupported reporter error"""


class MissingShareMailError(TwitterDataExtractorException):
    """Missing share mail error"""


class ExtractorDatabaseError(TwitterDataExtractorException):
    """Database operation error"""
