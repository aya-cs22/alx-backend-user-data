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
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded64 = base64.b64decode(encoded)
            decoded = decoded64.decode('utf-8')
        except BaseException:
            return None

        return decoded
