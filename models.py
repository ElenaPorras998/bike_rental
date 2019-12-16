# File containing the two database models used: Users and Bicycles
from . import db
from flask_login import UserMixin


# The UserMixin parameter makes the login of the Users instances possible.
# The class name matches the table's name.
# The properties match the table's columns.
class Users(UserMixin, db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    password = db.Column(db.String(150))
    add_date = db.Column(db.TIMESTAMP)

    def __init__(self, user_name, password, add_date):
        self.user_name = user_name
        self.password = password
        self.add_date = add_date


class Bicycles(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    latitude = db.Column(db.Numeric(50))
    longitude = db.Column(db.Numeric(50))
    add_date = db.Column(db.TIMESTAMP)

    def __init__(self, latitude, longitude, add_date):
        self.latitude = latitude
        self.longitude = longitude
        self.add_date = add_date

