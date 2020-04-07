'''
File name:    users.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file provides the blueprint for setting up and maintaining stores
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''
from flask import Blueprint,request,session,url_for,render_template,redirect
from model.alert import Alert
from model.user.user import User
import model.user.errors as UserErrors
import os

# Establish blueprint object for /users
user_blueprint = Blueprint('users',__name__)

# Handles requests routed to /users/register/
@user_blueprint.route('/register',methods=['GET','POST'])
def register_user():

    # If POST in request, user has already completed and submitted the registration form
    # After saving the user to database, the user is forwarded to a new alerts page
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            User.register_user(email,password)
            session['email'] = email
            return render_template('alerts/index.html')
            return email
        except UserErrors.UserError as e:
            # user errors are defined in model.user.errors
            return e.message

    # If no POST in request, user is presented new registration page to be completed
    return render_template('users/register.html')

# Handles requests routed to /users/login/
@user_blueprint.route('/login',methods=['GET','POST'])
def login_user():

    # If POST in request, then the user has submitted the form with content
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.is_login_valid(email,password):
                session['email'] = email
                alerts = Alert.find_many_by_email(email)
                return render_template('alerts/index.html',alerts=alerts)
        except UserErrors.UserError as e:
            # user errors are defined in model.user.errors
            return e.message

    # If no POST in request user is presented the login form to be completed
    return render_template('users/login.html')

# Handles requests routed to /users/logout/
@user_blueprint.route('/logout',methods=['GET','POST'])
def logout_user():

    # Remove session identifier and reset default alerts, forwarding user back to home page
    session['email'] = None
    alerts = Alert.find_many_by_email(os.getenv("ADMIN"))
    return render_template('home.html',alerts=alerts)
