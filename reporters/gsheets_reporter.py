from time import sleep

import gspread
from gspread.spreadsheet import Spreadsheet
from gspread.exceptions import SpreadsheetNotFound

from exceptions import MissingShareMailError
from models.user import User
from models.tweet import Tweet
from reporters.file_reporter import FileReporter
from utils import logger, ExtractedDataType


class GSheetsReporter(FileReporter):
    """Google Sheets report generator

    :type filename: str
    :param filename: Name or url of the output file
    :type extracted_data_type: ExtractedDataType
    :param extracted_data_type: Enum value for the extracted data type
    :type share_mail: str
    :param share_mail: Mail address to share Google Sheets document
    """

    def __init__(
        self, filename: str, extracted_data_type: ExtractedDataType, share_mail: str
    ) -> None:

        super().__init__(filename, extracted_data_type)

        self._share_mail = share_mail
        if not self._share_mail:
            raise MissingShareMailError("share_mail(sm) parameter is missing!")

        self._sheets_client = gspread.service_account(filename="credentials.json")
        self._gsheet = None

    def _save_user_data(self, extracted_data: User) -> None:
        """Save single user data

        :type extracted_data: User
        :param extracted_data: User object
        """

        gsheet = self._get_sheet()

        logger.info("Saving user data...")

        worksheet = gsheet.sheet1
        worksheet.clear()

        logger.info(extracted_data)

        self._add_user_header(worksheet)

        worksheet.append_row(FileReporter._get_user_row_data(extracted_data.data))

        worksheet.columns_auto_resize(
            start_column_index=1, end_column_index=len(self._user_data_header)
        )

    def _save_users_data(self, extracted_data: list[User]) -> None:
        """Save users/friends/followers data

        :type extracted_data: list
        :param extracted_data: List of Users(users/friends/followers)
        """

        is_friends_data = self._extracted_data_type == ExtractedDataType.FRIENDS

        if self._extracted_data_type == ExtractedDataType.USERS:
            logger.debug("Saving users data...")
        else:
            logger.debug(f"Saving {'friends' if is_friends_data else 'followers'} data...")

        gsheet = self._get_sheet()

        worksheet = gsheet.sheet1
        worksheet.clear()

        self._add_user_header(worksheet)

        for user_data_item in extracted_data:
            worksheet.append_row(FileReporter._get_user_row_data(user_data_item.data))
            GSheetsReporter._wait_for_quota_limit()

        worksheet.columns_auto_resize(
            start_column_index=1, end_column_index=len(self._user_data_header)
        )

    def _save_tweets_data(self, extracted_data: list[Tweet]) -> None:
        """Save tweets data

        :type extracted_data: list
        :param extracted_data: List of Tweets
        """

        logger.debug("Saving tweets data...")

        gsheet = self._get_sheet()

        worksheet = gsheet.sheet1
        worksheet.clear()

        self._add_tweet_header(worksheet)

        for tweet_data_item in extracted_data:
            worksheet.append_row(FileReporter._get_tweet_row_data(tweet_data_item.data))
            GSheetsReporter._wait_for_quota_limit()

        worksheet.columns_auto_resize(
            start_column_index=1, end_column_index=len(self._tweet_data_header)
        )

    def _add_user_header(self, worksheet: gspread.worksheet.Worksheet) -> None:
        """Add user data header

        :type worksheet: gspread.worksheet.Worksheet
        :param worksheet: Worksheet instance
        """

        worksheet.append_row(self._user_data_header)
        worksheet.format(f"A1:P1", {"textFormat": {"bold": True}})

    def _add_tweet_header(self, worksheet: gspread.worksheet.Worksheet) -> None:
        """Add tweet data header

        :type worksheet: gspread.worksheet.Worksheet
        :param worksheet: Worksheet instance
        """

        if self._extracted_data_type == ExtractedDataType.USER_TWEETS:
            self._tweet_data_header.remove("Author")

        worksheet.append_row(self._tweet_data_header)
        worksheet.format(f"A1:L1", {"textFormat": {"bold": True}})

    def _get_sheet(self) -> Spreadsheet:
        """Create or open spreadsheet

        :rtype: Spreadsheet
        :returns: Spreadsheet instance
        """

        if self._gsheet is None:
            try:
                logger.info(f"Opening sheet {self._filename}...")

                if "docs.google.com" in self._filename:
                    self._gsheet = self._sheets_client.open_by_url(self._filename)
                else:
                    self._gsheet = self._sheets_client.open(self._filename)

            except SpreadsheetNotFound:
                logger.error(f"Spreadsheet could not be found with name: {self._filename}")
                logger.info(f"Creating a sheet with name: {self._filename}")
                self._gsheet = self._sheets_client.create(self._filename)

                self._gsheet.share(self._share_mail, perm_type="user", role="writer")

        return self._gsheet

    @staticmethod
    def _wait_for_quota_limit():
        """Sleep 1 second between write requests"""

        sleep(1)
