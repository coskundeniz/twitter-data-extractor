from typing import Union

from exceptions import UnsupportedReporterError
from reporters import file_reporter
from reporters import database_reporter
from reporters.csv_reporter import CsvReporter
from reporters.excel_reporter import ExcelReporter
from reporters.gsheets_reporter import GSheetsReporter
from reporters.mongodb_reporter import MongoDBReporter
from reporters.sqlite_reporter import SQLiteReporter
from utils import get_configuration, get_extracted_data_type


class ReporterFactory:
    """Factory class for url readers"""

    @staticmethod
    def get_reporter(
        cmdline_args: "Namespace",
    ) -> Union[file_reporter.FileReporter, database_reporter.DatabaseReporter]:  # noqa: F821
        """Get specific reporter

        Raises UnsupportedReporterError if output format is not supported.

        :type cmdline_args: Namespace
        :param cmdline_args: Command line args returned by ArgumentParser
        :rtype: file_reporter.FileReporter | database_reporter.DatabaseReporter
        :returns: Concrete FileReporter or DatabaseReporter object
        """

        reporter = None

        # config = get_configuration(cmdline_args.configfile)

        # if cmdline_args.useconfig:
        #     output_type = config["output_type"]
        #     output_file = config["output_file"]
        # else:
        output_type = cmdline_args.output_type
        output_file = cmdline_args.output_file

        extracted_data_type = get_extracted_data_type(cmdline_args)

        if output_type == "csv":
            reporter = CsvReporter(output_file, extracted_data_type)
        elif output_type == "xlsx":
            reporter = ExcelReporter(output_file, extracted_data_type)
        elif output_type == "gsheets":
            reporter = GSheetsReporter(output_file, extracted_data_type, cmdline_args.share_mail)
        elif output_type == "mongodb":
            reporter = MongoDBReporter(extracted_data_type)
        elif output_type == "sqlite":
            reporter = SQLiteReporter(extracted_data_type)
        else:
            message = (
                "Unsupported output file! Should be one of csv, excel, gsheets, mongodb or sqlite"
            )
            raise UnsupportedReporterError(message)

        return reporter
