from sqlalchemy import func
from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, )
    name = db.Column(db.String(100), unique=True, )
    password = db.Column(db.String(100), nullable=False)
    notes=db.relationship("Note")
class Note (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date=db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
