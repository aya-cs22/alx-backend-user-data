#!/usr/bin/env python3
"""
auth
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    '''hashing pswd'''
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def _generate_uuid() -> str:
    '''return a string representation of a new UUID'''
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        '''init'''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''registering a user'''
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass_hashed = _hash_password(password)
            new_user = self._db.add_user(email=email,
                                         hashed_password=pass_hashed)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        '''validate user'''
        try:
            user = self._db.find_user_by(email=email)
            bytes_password = password.encode("utf-8")
            return bcrypt.checkpw(bytes_password, user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        '''creating a session'''
        try:
            user = self._db.find_user_by(email=email)
            id = _generate_uuid()
            user.session_id = id
            return id
        except NoResultFound:
            pass
# #!/usr/bin/env python3
# """ Authentication Module """

# import bcrypt
# from db import DB
# from sqlalchemy.orm.exc import NoResultFound
# from typing import Union
# from user import User
# from uuid import uuid4


# def _hash_password(password: str) -> str:
#     """Hash password"""
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed_password


# class Auth:
#     """Auth class to interact with the authentication database.
#     """

#     def __init__(self):
#         self._db = DB()

#     def register_user(self, email: str, password: str) -> User:
#         """Register a new user with the given email and password."""
#         try:
#             self._db.find_user_by(email=email)
#             raise ValueError(f"User {email} already exists")
#         except Exception:
#             hash_password = self._hash_password(password)
#             user = self._db.add_user(email, hash_password)
#             return user
