from flask import Blueprint,request,session,url_for,render_template,redirect
import os

from model.alert import Alert
from model.user.user import User
import model.user.errors as UserErrors

user_blueprint = Blueprint('users',__name__)

@user_blueprint.route('/register',methods=['GET','POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.register_user(email,password)
            session['email'] = email
            return render_template('alerts/index.html')
            return email

        except UserErrors.UserError as e:
            return e.message

    return render_template('users/register.html')

@user_blueprint.route('/login',methods=['GET','POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email,password):
                session['email'] = email
                alerts = Alert.find_many_by_email(email)
                return render_template('alerts/index.html',alerts=alerts)

        except UserErrors.UserError as e:
            return e.message

    return render_template('users/login.html')

@user_blueprint.route('/logout',methods=['GET','POST'])
def logout_user():
    session['email'] = None
    alerts = Alert.find_many_by_email(os.getenv("ADMIN"))
    return render_template('home.html',alerts=alerts)
