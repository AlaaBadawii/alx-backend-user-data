#!/usr/bin/env python3
""" filtered_logger module """
import re


def filter_datum(
        fields: list[str],  # representing all fields to obfuscate
        redaction: str,  # representing by what the field will be obfuscated
        message: str,  # representing the log line
        separator: str):
    """ returns the log message obfuscated """
    for key in fields:
        pattern = rf'({key}=)[^{separator}]+'
        message = re.sub(pattern, rf'\1{redaction}', message)
    return message
