'''
File name:    user.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file establishes the User class with attributes and methods to facilitate user registration
              and subsequent login.
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''
import uuid
from dataclasses import dataclass, field
from typing import Dict
from model.model import Model
from common.utils import Utils
import model.user.errors as UserErrors

# User class established as a dataclass which extends the Model class
@dataclass
class User(Model):
    # Constructor implied for dataclass based on attributes
    collection: str = field(init=False,default='users')
    email: str
    password: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    # Method returns User object based on email address
    @classmethod
    def find_by_email(cls,email: str) -> "User":
        try:
            return cls.find_one_by('email',email)
        except TypeError:
            raise UserErrors.UserNotFoundError('A user with this email was not found.')

    # Method attempts to register a new user - unless they are registered which raises an error message
    @classmethod
    def register_user(cls,email: str, password: str) -> bool:
        # First verify that the email is a valid email address
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailERror('The email does not have the right format.')

        # Next check to see if the email address is already a registered user
        if (cls.find_by_email(email) != None):
            raise UserErrors.UserAlreadyRegisteredError('The email you used to register already exists.')
        else:
            user = User(email,Utils.hash_password(password))
            print(user)
            User(email,Utils.hash_password(password)).save_to_mongo()

        return True

    # Method creates json object for User
    def json(self) -> Dict:
        return {
            '_id': self._id,
            'email': self.email,
            'password': self.password
        }

    # Method returns True if email and password are valid
    @classmethod
    def is_login_valid(cls, email: str, password : str) -> bool:
        # Find the user in the database
        user = cls.find_by_email(email)

        # Verify password
        if not Utils.check_hashed_password(password,user.password):
            raise UserErrors.IncorrectPasswordError('Your password was incorrect.')

        return True