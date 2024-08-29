#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string."""
    password_byte = password.encode()
    hashed_password = bcrypt.hashpw(password_byte, bcrypt.gensalt())
    return hashed_password


# def is_valid(hashed_password: bytes, password: str) -> bool:
#     pass