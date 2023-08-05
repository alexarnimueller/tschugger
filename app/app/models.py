from __init__ import db


class Member(db.Model):
    id = db.Column(db.Integer, db.ForeignKey("app_user.id"), primary_key=True, nullable=False)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=False)
    scoutname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True)
    phone = db.Column(db.String(64), unique=True)
    notes = db.Column(db.Text, default="")
    img = db.Column(db.String(64))

    def __repr__(self):
        return "<Member %r %r / %r>" % (self.firstname, self.lastname, self.scoutname)


class AppUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<User %r>" % (self.username)
