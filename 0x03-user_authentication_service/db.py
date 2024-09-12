#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db",
                                     echo=False)
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
        """
        Create a User object and save it to the database
        Args:
            email (str): user's email address
            hashed_password (str): password hashed by bcrypt's hashpw
        Return:
            Newly created User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Return a user who has an attribute matching the attributes passed
        as arguments
        Args:
            attributes (dict): a dictionary of attributes to match the user
        Return:
            matching user or raise error
        """
        all_users = self._session.query(User)
        for k, v in kwargs.items():
            if k not in User.__dict__:
                raise InvalidRequestError
            for usr in all_users:
                if getattr(usr, k) == v:
                    return usr
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes
        Args:
            user_id (int): user's id
            kwargs (dict): dict of key, value pairs representing the
                           attributes to update and the values to update
                           them with
        Return:
            No return value
        """
        try:
            usr = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()
        for k, v in kwargs.items():
            if hasattr(usr, k):
                setattr(usr, k, v)
            else:
                raise ValueError
        self._session.commit()
        # #!/usr/bin/env python3
# """ Database for ORM """
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import InvalidRequestError
# from sqlalchemy.orm.exc import NoResultFound
# from typing import TypeVar
# from user import Base, User


# class DB:
#     """ DB Class for Object Reational Mapping """

#     def __init__(self):
#         """ Constructor Method """
#         self._engine = create_engine("sqlite:///a.db", echo=False)
#         Base.metadata.drop_all(self._engine)
#         Base.metadata.create_all(self._engine)
#         self.__session = None

#     @property
#     def _session(self):
#         """ Session Getter Method """
#         if self.__session is None:
#             DBSession = sessionmaker(bind=self._engine)
#             self.__session = DBSession()
#         return self.__session

#     def add_user(self, email: str, hashed_password: str) -> User:
#         """Implementation to add user to the database"""
#         user = User(email=email, hashed_password=hashed_password)
#         self._session.add(user)
#         self._session.commit()
#         return user

#     def find_user_by(self, **kwargs) -> User:
#         """To find a user in the Users table"""
#         try:
#             user = self.__session.query(User).filter_by(**kwargs).first()
#             if user is None:
#                 raise NoResultFound
#             return user
#         except NoResultFound:
#             raise NoResultFound
#         except InvalidRequestError:
#             raise InvalidRequestError()
#         except Exception as e:
#             raise Exception(e)

#     def update_user(self, user_id: int, **kwargs) -> None:
#         """Update user information in the database"""
#         try:
#             user = self.find_user_by(id=user_id)
#             for key, value in kwargs.items():
#                 if not hasattr(user, key):
#                     raise ValueError
#                 setattr(user, key, value)
#             self.__session.commit()
#         except NoResultFound:
#             raise NoResultFound
