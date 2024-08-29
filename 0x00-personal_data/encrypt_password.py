#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes the given password using bcrypt.
    Args:
        password (str): The password to be hashed.
    Returns:
        bytes: The hashed password.
    """
    byt_psd = password.encode()
    salted = bcrypt.hashpw(byt_psd, bcrypt.gensalt())
    return salted
# def hash_password(password: str) -> bytes:
#     """returns a salted, hashed password, which is a byte string."""
#     password_byte = password.encode()
#     hashed_password = bcrypt.hashpw(password_byte, bcrypt.gensalt())
#     return hash_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    pass