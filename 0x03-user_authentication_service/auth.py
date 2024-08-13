#!/usr/bin/env python3
""" auth module """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ takes in a password string arguments and returns bytes.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ return a User object.
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User <user's email> already exists")
        except NoResultFound:
            hashed_password = _hash_password(password=password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
