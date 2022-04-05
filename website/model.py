from . import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    # email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String,  unique=True)
    password = db.Column(db.String(30))
