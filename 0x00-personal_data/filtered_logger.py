#!/usr/bin/env python3
"""modul"""
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return (message)


def get_logger() -> logging.Logger:
    """Create logger"""
    loger = logging.getLogger("user_data")
    loger.setLevel(logging.INFO)
    loger.propagate = False
    smart_handler = logging.StreamHandler()
    formater = RedactingFormatter(fields=PII_FIELDS)
    smart_handler.setFormatter(formater)
    loger.addHandler(smart_handler)
    return loger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to secure database"""
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')
    db = mysql.connector.connection.MySQLConnection(
        user=user,
        password=password,
        host=host,
        database=database
    )
    return db


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter"""
        mes = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, mes, self.SEPARATOR)


def main():
    """
    Obtain a database connection using get_db, retrieves all rows
    in the users table, and logs each row with a formatted message.
    """
    logger = get_logger()

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM users;")
        field_names = [i[0] for i in cursor.description]
        for row in cursor:
            message = ''.join(f'{field}={str(value)}; ' for field,
                              value in zip(field_names, row))
            logger.info(message.strip())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    main()
