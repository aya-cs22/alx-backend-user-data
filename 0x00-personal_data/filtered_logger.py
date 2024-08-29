#!/usr/bin/env python3
"""modul"""
import re


def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    pattern = r'(?:{separator}={field})[^{separator}]+' \
        .format(separator=separator, field='|'.join(fields))
    return re.sub(pattern, redaction, message)
