#!/usr/bin/env python3
"""DB module.
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ takes in arbitrary keyword arguments and
        returns the first row found in the users table
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except NoResultFound:
            self._session.rollback()
            raise
        except InvalidRequestError:
            self._session.rollback()
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates a user based on a given id.
        """
        try:
            if not kwargs:
                raise ValueError

            user = self.find_user_by(id=user_id)
            if user is None:
                return

            for k, v in kwargs.items():
                if hasattr(user, k):
                    setattr(user, k, v)
                else:
                    raise ValueError

            self._session.commit()

        except (NoResultFound, InvalidRequestError) as e:
            self._session.rollback()
            raise e
        except Exception as e:
            self._session.rollback()
            raise ValueError
