'''
File name:    alert_updater.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file initiates a review of all alerts which users have saved in the application and sends emails
              to users where prices have reached their desired price or below.
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''
from model.alert import Alert

# Collecting all alerts in the application
alerts = Alert.all()

# Checking prices and sending notifications where appropriate
for alert in alerts:
    alert.load_item_price()
    print(alert.item.price)
    alert.notifiy_if_price_reached()

# Sending notification to console if no alerts exist yet
if not alerts:
    print("No alerts have been created.  Add an item and an alert to begin!")
