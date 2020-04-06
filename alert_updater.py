from model.alert import Alert
from dotenv import load_dotenv

alerts = Alert.all()

for alert in alerts:
    alert.load_item_price()
    print(alert.item.price)
    alert.notifiy_if_price_reached()

if not alerts:
    print("No alerts have been created.  Add an item and an alert to begin!")
