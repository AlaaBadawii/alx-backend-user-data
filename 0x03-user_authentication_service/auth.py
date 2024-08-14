#!/usr/bin/env python3
""" auth module """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid


def _hash_password(password: str) -> bytes:
    """ takes in a password string arguments and returns bytes.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt)


def _generate_uuid() -> str:
    """Generate and return a string representation of a new UUID."""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """ chec the password if the email exists
        """
        try:
            user = self._db.find_user_by(email=email)
            pwd = password.encode('utf-8')
            return bcrypt.checkpw(pwd, user.hashed_password)
        except(NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """ Create a session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (NoResultFound, InvalidRequestError):
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Get user by session_id or return None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except(InvalidRequestError, NoResultFound):
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroy a session
        """
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except(InvalidRequestError, NoResultFound, ValueError):
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ Reset user's current password
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except (NoResultFound, InvalidRequestError):
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ update the user's password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password)
            self._db.update_user(user.id, reset_token=None)
            return None
        except (NoResultFound, InvalidRequestError, ValueError):
            raise ValueError
