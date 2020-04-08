'''
File name:    utils.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file establishes the Utils class containing static methods as are needed throughout the
              application.
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''
import re
from passlib.hash import pbkdf2_sha512

class Utils:
    # Determines whether or not a string object is a valid email address
    @staticmethod
    def email_is_valid(email: str) -> bool:
        email_address_matcher = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        return True if email_address_matcher.match(email) else False

    # Method provides a string which is the sha512 encryption of a user's password
    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha512.encrypt(password)

    # Method checks a given password to see if it is equal to the user's stored password
    @staticmethod
    def check_hashed_password(password: str, hashed_password: str) -> bool:
        return pbkdf2_sha512.verify(password,hashed_password)