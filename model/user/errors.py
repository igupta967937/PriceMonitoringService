'''
File name:    errors.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file establishes the Error classes as needed for user interactions.
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''

class UserError(Exception):
    def __init__(self,message):
        self.message = message

class UserNotFoundError(UserError):
    pass


class UserAlreadRegisteredError(UserError):
    pass

class InvalidEmailError(UserError):
    pass

class IncorrectPasswordError(UserError):
    pass