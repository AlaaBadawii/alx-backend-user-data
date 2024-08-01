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
