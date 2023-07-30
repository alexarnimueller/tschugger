from datetime import datetime
from __init__ import db


class AppUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(64), nullable=False, default="Tschugger")
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True)
    phone = db.Column(db.String(64), unique=True)
    notes = db.Column(db.Text, default="")
    joined = db.Column(db.DateTime, default=datetime.now())
    token = db.Column(db.String(16), default="")

    def __repr__(self):
        return "<Member %r %r>" % (self.firstname, self.lastname)
