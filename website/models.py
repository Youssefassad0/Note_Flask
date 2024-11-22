from sqlalchemy import func
from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'User_note'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class RA(UserMixin, db.Model):
    __tablename__ = "RA"
    Number = db.Column(db.String(20), primary_key=True)
    Close_Date = db.Column(db.DateTime)
    Close_User = db.Column(db.String(50))
    Date_Out = db.Column(db.DateTime)
    Date_In = db.Column(db.DateTime)
    Return_Date = db.Column(db.DateTime)
    Station_Out = db.Column(db.String(50))
    Station_In = db.Column(db.String(50))
    Return_Station = db.Column(db.String(50))
    Return_Place = db.Column(db.String(50))
    Return_Date = db.Column(db.Date)

class RA_Vehicles(UserMixin,db.Model):
    __tablename__ = "RA_Vehicles"
    RA = db.Column(db.String(20), primary_key=True)  
    Unit_Number = db.Column(db.String(50))
    Plate_Number = db.Column(db.String(50))
    Station_out = db.Column(db.String(50))
    Data_Out = db.Column(db.DateTime)
    Station_In = db.Column(db.String(50))
    Data_In = db.Column(db.DateTime)

