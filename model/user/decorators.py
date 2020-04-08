'''
File name:    decorators.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file establishes callable functions to be used in handling http requests.
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''
import functools
import os
from typing import Callable
from flask import session, flash, redirect, url_for, request, current_app

# Function checks the present session to verify that the user's email is registered with a current session
def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args,**kwargs):
        if not session.get('email'):
            flash('You need to be signed in for this page.','danger')
            return redirect(url_for('users.login_user'))
        return f(*args,**kwargs)

    return decorated_function

# Function checks that the user's email registered in the current session is the ADMIN email
def requires_admin(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('email') != os.getenv("ADMIN"):
            flash('You need to be an administrator to access this page.','danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)

    return decorated_function


