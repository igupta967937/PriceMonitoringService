from flask import Flask, render_template,request
from model.alert import Alert
from views.alerts import alert_blueprint
from views.stores import store_blueprint
from views.users import user_blueprint
from dotenv import load_dotenv

import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

@app.route('/')
def home():
    alerts = Alert.find_many_by_email(os.getenv("ADMIN"))
    return render_template('home.html',alerts=alerts)

app.register_blueprint(alert_blueprint,url_prefix="/alerts")
app.register_blueprint(store_blueprint,url_prefix="/stores")
app.register_blueprint(user_blueprint,url_prefix="/users")

if __name__ == '__main__':
    app.run(debug=False)

