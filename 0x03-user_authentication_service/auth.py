#!/usr/bin/env python3
""" auth module """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ takes in a password string arguments and returns bytes.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt)
