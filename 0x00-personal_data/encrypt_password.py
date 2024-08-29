#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string."""
    password_byte = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_byte, bcrypt.gensalt())
    return hash_password
