#!/usr/bin/env python3
"""Auth class"""
from typing import List, TypeVar
from flask import request
import os


class Auth:
    """This class is the template for all authentication system"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determine whether the path requires verification"""
        if path is None:
            return True
        if not excluded_paths or excluded_paths is None:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the request verification header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Determine the current user based on the request"""
        return None

    def session_cookie(self, request=None):
        """ that returns a cookie value from a request"""
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        if session_name is None:
            return None
        return request.cookies.get(session_name)
