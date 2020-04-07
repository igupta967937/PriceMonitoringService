'''
File name:    stores.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file provides the blueprint for setting up and maintaining stores
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''
import json
import os
from flask import Blueprint, render_template,request,url_for, redirect
from model.store import Store
from model.user.decorators import requires_admin, requires_login

# Establish blueprint object for /stores objects
store_blueprint = Blueprint('stores', __name__)

# Handles requests routed to /stores/ and requires_login from model.users.decorators
@store_blueprint.route('/')
@requires_login
def index():

    # Get a list of all stores from database
    stores = Store.all()

    # Get admin email address from environment variables
    admin_email = os.getenv("ADMIN")

    # Prepare a list of stores
    for store in stores:
        print(store.name)

    # Present user with page containing list of stores with admin email in memory
    return render_template('stores/index.html', stores=stores,admin=admin_email)

# Handles requests routed to /stores/new/ and requires_login from model.users.decorators
@store_blueprint.route('/new',methods=['GET','POST'])
@requires_admin
def create_store():

    # If POST then the user has visited the form already and submitted a new store
    # After saving the new store, the user is forwarded back to '/stores/'
    if request.method == 'POST':
        name= request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'].replace("'","\""))
        Store(name, url_prefix, tag_name, query).save_to_mongo()
        return redirect(url_for('.index'))

    # If no POST then user is givne the new store form to complete and submit
    return render_template('/stores/new_store.html')

# Handles requests routed to /stores/edit/ requires_login and requires_admin from model.users.decorators
@store_blueprint.route('/edit/<string:store_id>',methods=['GET','POST'])
@requires_admin
def edit_store(store_id):

    # Getting store from database
    store = Store.get_by_id(store_id)

    # If POST then edit form has been completed already
    # After store edit form saved, user redirected to '/stores/'
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'].replace("'","\""))
        store.name = name
        store.url_prefix = url_prefix
        store.tag_name = tag_name
        store.query = query
        store.save_to_mongo()
        return redirect(url_for('.index'))

    # If no POST, then user is presented with the edit store form to be completed.
    return render_template('stores/edit_store.html',store=store)

# Handles requests routed to /stores/edit/ requires_login and requires_admin from model.users.decorators
@store_blueprint.route('/delete/<string:store_id>')
def delete_store(store_id):

    # Remove the store from the database
    Store.get_by_id(store_id).remove_from_mongo()

    # return the user to '/stores/'
    return redirect(url_for('.index'))