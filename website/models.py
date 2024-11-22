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

