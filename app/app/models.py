from __init__ import db


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(64), nullable=False, default="Tschugger")
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    scoutname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True)
    phone = db.Column(db.String(64), unique=True)
    notes = db.Column(db.Text, default="")
    img = db.Column(db.String(64))
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Member %r %r / %r>" % (self.firstname, self.lastname, self.scoutname)
