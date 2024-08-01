#!/usr/bin/env python3
""" filtered_logger module"""
import re
from typing import List
import logging
import os
import mysql.connector
from mysql.connector import errorcode

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')
patterns = {
    'extract': lambda x, y: r'(?p<field>{})=[^{}]*'.format('|'.join(y), x),
    'replace': lambda x: r'\g<field>={}'.format(x),
}


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    extract, replace = (patterns['extract'], patterns['replace'])
    return re.sub(extract(separator, fields), replace(redaction), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ("name", "levelname", "asctime", "message")
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format - format the record
        """
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt
