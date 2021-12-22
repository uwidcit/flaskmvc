from App.models import Alert
from . import db


def get_alert_by_id(id):
    print(f"Getting alert: {id}")
    alert = Alert.query.filter_by(id=id).first()
    return alert