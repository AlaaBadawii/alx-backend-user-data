#!/usr/bin/env python3
""" session_auth module
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """ authentication mechanism
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for a user_id
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value
        """
        session_id = self.session_cookie(request=request)
        user_id = self.user_id_for_session_id(session_id=session_id)
        user = User.get(user_id)

        return user

    def destroy_session(self, request=None):
        """ deletes the user session / logout
        """
        if request is None:
            return False

        session_id = self.session_cookie(request=request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id=session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
