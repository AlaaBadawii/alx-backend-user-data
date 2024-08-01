#!/usr/bin/env python3
""" filtered_logger module """
import re
import logging


def filter_datum(
        fields: list[str],  # representing all fields to obfuscate
        redaction: str,  # representing by what the field will be obfuscated
        message: str,  # representing the log line
        separator: str):
    """ returns the log message obfuscated """
    for field in fields:
        message = re.sub(rf"{field}=.+?{separator}",
                         f"{field}={redaction}{separator}",
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list[str]):
        """ RedactingFormatter constructor """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ RedactingFormatter format method """
        return filter_datum(
            self.fields, self.REDACTION,
            super().format(record), self.SEPARATOR)
