'''
File name:    __init__.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file initiates a pricing service application.  The web application allows users to scan the internet
              for the current prices of products they are interested in buying, notifying them when the price reaches
              their desired price.  This application was originally produced in connection with a Python full-stack
              course, but is now being developed as a Java full stack application under the name BargainBuyClub.com
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''
from flask import Flask, render_template,request

from common.database import Database
from model.alert import Alert
from views.alerts import alert_blueprint
from views.stores import store_blueprint
from views.users import user_blueprint
from dotenv import load_dotenv

import os

# Loading environment variables (.env)
load_dotenv()

# Initiating Flask server.  Secret key provided with environment variables.
app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

# Loading home page to initiate the application
@app.route('/')
def home():
    alerts = Alert.find_many_by_email(os.getenv("ADMIN")) # Alerts for ADMIN provide home page examples.
    return render_template('home.html',alerts=alerts)

# Provide structure for application with branches for alerts, stores, and users
app.register_blueprint(alert_blueprint,url_prefix="/alerts")
app.register_blueprint(store_blueprint,url_prefix="/stores")
app.register_blueprint(user_blueprint,url_prefix="/users")

if __name__ == '__main__':
    app.run(debug=False)
