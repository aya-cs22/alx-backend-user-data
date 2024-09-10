#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User
from user import Base
from sqlalchemy.exc import NoResultFound, InvalidRequestError


class DB:
    """DB class
    """

    def __init__(self):
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Implementation to add user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs):
        """Find a user by given attributes"""
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound()
        except Exception as e:
            raise InvalidRequestError(e)

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user with the given user_id and attributes."""
        # 1. Find the user by ID
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise NoResultFound("No user found with the given ID.")
        
        # 2. Check for valid attributes and update the user
        for attr, value in kwargs.items():
            if not hasattr(user, attr):
                raise ValueError(f"Invalid attribute: {attr}")
            setattr(user, attr, value)
        
        # 3. Commit the changes to the database
        try:
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise RuntimeError(f"An error occurred while committing the changes: {e}")
