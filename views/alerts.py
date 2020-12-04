'''
File name:    alerts.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file provides the blueprint for user login and alert operations.
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''
from flask import Blueprint,render_template,request,redirect,url_for,session
from model.alert import Alert
from model.user.user import User
from model.store import Store
from model.item import Item
from model.user.decorators import requires_login

# Establish blueprint object for /alerts objects
alert_blueprint = Blueprint('alerts',__name__)


# Handles requests routed to /alerts/ and requires_login from model.users.decorators
@alert_blueprint.route('/')
@requires_login
def index():

    # Get alerts from database (null if none)
    alerts = Alert.find_many_by_email(session['email'])
    for alert in alerts:
        print(alert.user_email)

    # Render alerts template with alerts from database
    return render_template('alerts/index.html', alerts = alerts) # Render alerts template with alerts from database


# Handles requests routed to /alerts/new/ and requires_login from model.users.decorators
@alert_blueprint.route("/new",methods=['GET','POST'])
@requires_login
def new_alert():

    # If POST method included in the request, a new alert needs to be saved
    # After saving the new alert from the POST, user redirected to their alerts list at '/'
    if request.method == 'POST':
        alert_name = request.form['name']
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'])
        store = Store.find_by_url(item_url)
        item = Item(item_url, store.tag_name, store.query)
        item.load_price()
        item.save_to_mongo()
        Alert(alert_name, item._id, price_limit,session['email']).save_to_mongo()

        return redirect(url_for('.index'))

    # If POST was not included in the request, form is provided for user to enter new alert information
    return render_template('/alerts/new_alert.html')

# Handles requests routed to /alerts/edit/ and requires_login from model.users.decorators
@alert_blueprint.route('/edit/<string:alert_id>', methods = ['GET','POST'])
@requires_login
def edit_alert(alert_id):

    # Get the alert information from the database (alert_id part of GET request)
    alert = Alert.get_by_id(alert_id)
    item = Item.get_by_id(alert.item_id)

    # POST method is used once changes have been made on the edit alert form
    # After saving the updated alert, the user is forwarded back to alerts home '/'
    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])
        alert.price_limit = price_limit
        alert.save_to_mongo()
        return redirect(url_for('.index'))

    # Where GET request only, user is directed to the edit alert page
    return render_template('alerts/edit_alert.html',alert = alert)

# Handles requests routed to /alerts/delete/
@alert_blueprint.route('/delete/<string:alert_id>')
def delete_alert(alert_id):

    # Remove alert from database
    Alert.get_by_id(alert_id).remove_from_mongo()

    # Redirect to alerts home page
    return redirect(url_for('.index'))
