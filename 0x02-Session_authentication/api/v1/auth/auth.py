#!/usr/bin/env python3
"""Auth module
"""
from flask import request as res
from typing import List, TypeVar
import os


class Auth():
    """ Auth class to manage the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ for authentication
        """
        if excluded_paths is None:
            return True

        if ((path == "/api/v1/status" or path == "/api/v1/status/")
                and "/api/v1/status/" in excluded_paths):
            return False

        if (path is None
                or path not in excluded_paths):
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """ authorization_header
        """
        header_key = 'Authorization'

        if request is None or header_key not in res.headers:
            return None
        return res.headers[header_key]

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user
        """
        return None

    def session_cookie(self, request=None):
        """  returns a cookie value from a request:
        """
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
