#!/usr/bin/env python3
"""Auth class"""
from typing import List, TypeVar
from flask import request


class Auth:
    """This class is the template for all authentication system"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determine whether the path requires verification"""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns the request verification header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Determine the current user based on the request"""
        return None
