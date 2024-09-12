#!/usr/bin/env python3
""" Database for ORM """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
from user import Base, User


class DB:
    """ DB Class for Object Reational Mapping """

    def __init__(self):
        """ Constructor Method """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    
    @property
    def _session(self):
        """ Session Getter Method """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def find_user_by(self, **kwargs) -> User:
        """To find a user in the Users table"""
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user information in the database"""
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError
                setattr(user, key, value)
            self.__session.commit()
        except NoResultFound:
            raise NoResultFound


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
