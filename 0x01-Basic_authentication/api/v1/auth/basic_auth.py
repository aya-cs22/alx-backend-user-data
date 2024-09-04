#!/usr/bin/env python3
"""class BasicAuth"""
from api.v1.auth.auth import Auth


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
