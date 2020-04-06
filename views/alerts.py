from flask import Blueprint,render_template,request,redirect,url_for,session
import json

from model.alert import Alert
from model.store import Store
from model.item import Item
from model.user.decorators import requires_login

alert_blueprint = Blueprint('alerts',__name__)

@alert_blueprint.route('/')
@requires_login
def index():
    alerts = Alert.find_many_by_email(session['email'])
    for alert in alerts:
        print(alert.user_email)
    return render_template('alerts/index.html', alerts = alerts)

@alert_blueprint.route("/new",methods=['GET','POST'])
@requires_login
def new_alert():
    if request.method == 'POST':
        alert_name = request.form['name']
        print(alert_name)
        item_url = request.form['item_url']
        print(item_url)
        price_limit = float(request.form['price_limit'])
        print(price_limit)
        store = Store.find_by_url(item_url)
        print(store.tag_name)
        print(store.query)
        item = Item(item_url, store.tag_name, store.query)
        print(item.url)
        print(item.tag_name)
        item.load_price()
        print(item.price)
        item.save_to_mongo()

        Alert(alert_name, item._id, price_limit,session['email']).save_to_mongo()

        return redirect(url_for('.index'))


    return render_template('/alerts/new_alert.html')

@alert_blueprint.route('/edit/<string:alert_id>', methods = ['GET','POST'])
@requires_login
def edit_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    item = Item.get_by_id(alert.item_id)

    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])
        alert.price_limit = price_limit
        alert.save_to_mongo()
        return redirect(url_for('.index'))

    return render_template('alerts/edit_alert.html',alert = alert)

@alert_blueprint.route('/delete/<string:alert_id>')
def delete_alert(alert_id):
    Alert.get_by_id(alert_id).remove_from_mongo()
    return redirect(url_for('.index'))