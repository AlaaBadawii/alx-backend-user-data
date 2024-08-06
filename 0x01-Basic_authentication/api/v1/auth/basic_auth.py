#!/usr/bin/env python3
""" basic_auth module
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ basic_auth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if (authorization_header is None
                or type(authorization_header) is not str
                or not authorization_header.startswith("Basic ")):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """ Returns the decoded value of a Base64 string
        """
        if (base64_authorization_header is None
                or type(base64_authorization_header) is not str):
            return None
        try:
            res = base64.b64decode(base64_authorization_header).decode('utf-8')
            return res
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """returns the user email and password from the Base64 decoded value.
        """
        if (decoded_base64_authorization_header is None
                or type(decoded_base64_authorization_header) is not str
                or ':' not in decoded_base64_authorization_header):
            return (None, None)

        (v1, v2) = decoded_base64_authorization_header.split(':')
        return (v1, v2)
