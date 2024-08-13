#!/usr/bin/env python3
""" user moduel """
from sqlalchemy.orm import declarative_base, create_session
from sqlalchemy import Integer, String, create_engine, Column

Base = declarative_base()


class User(Base):
    """ users table
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
