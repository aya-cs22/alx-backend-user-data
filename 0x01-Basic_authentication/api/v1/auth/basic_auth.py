#!/usr/bin/env python3
"""class BasicAuth"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """The BasicAuth class inherits from Auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract the Base64 encoded part from the authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                               str) -> str:
        """Decode the Base64 string into a UTF-8 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded64 = b64decode(encoded)
            decoded = decoded64.decode('utf-8')
        except Exception:
            return None

        return decoded

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Extract user email and password"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        try:
            email, password = decoded_base64_authorization_header.split(':', 1)
            return email, password
        except ValueError:
            return None, None

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Return the User instance based on email and password"""
        if not isinstance(user_email, str) or user_email is None:
            return None
        if not isinstance(user_pwd, str) or user_pwd is None:
            return None
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        if not user:
            return None
        for u in user:
            if u.is_valid_password(user_pwd):
                return u
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the User instance for the request"""
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header
        )

        if base64_auth_header is None:
            return None
        decoded_auth_header = self.decode_base64_authorization_header(base64_auth_header)
        if decoded_auth_header is None:
            return None
        email, password = self.extract_user_credentials(decoded_auth_header)
        if email is None or password is None:
            return None
        return self.user_object_from_credentials(email, password)
