#!/usr/bin/env python3
""" filtered_logger module """
import logging
import re
from typing import List
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    return sub(fields, redaction, message, separator)


def sub(fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """ helper function """
    for field in fields:
        pattern = rf'({field}=).*?({separator})'
        message = re.sub(pattern, fr'\1{redaction}\2', message)
    return message


def get_logger() -> logging.Logger:
    """get_logger function that takes no arguments
    and returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    streamHandler = logging.StreamHandler()
    streamHandler.formatter(RedactingFormatter)
    logger.addHandler(streamHandler)
    logger.propagate = False

    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats a LogRecord.
        """
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt

    def format(self, record: logging.LogRecord) -> str:
        """formats a LogRecord.
        """
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt
