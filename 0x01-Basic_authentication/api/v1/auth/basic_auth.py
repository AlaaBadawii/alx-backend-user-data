#!/usr/bin/env python3
""" basic_auth module
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ basic_auth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ eturns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if (authorization_header is None
                or type(authorization_header) is not str
                or not authorization_header.startswith("Basic ")):
            return None
        return authorization_header[6:]
