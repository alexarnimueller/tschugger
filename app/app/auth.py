import os
import functools
import logging
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from forms import UserRegistrationForm, LoginForm
from models import AppUser, Member

from __init__ import db


bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = AppUser.query.filter_by(id=user_id).first_or_404(
            description="There is no user with ID {}".format(user_id)
        )


@bp.route("/access", methods=("GET", "POST"))
def access():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        password = request.form["password"]
        if os.getenv("ACCESS_PASSWORD") == password:
            session["access"] = True
            return redirect(url_for("auth.register"))

        flash("Incorrect password!", "danger")
    return render_template("auth/access.html")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if session.get("access"):
        error = ""
        form = UserRegistrationForm()
        if form.validate_on_submit():
            blacklist = open(url_for("static", filename="blacklist.txt"), "r").readlines()
            user = AppUser()
            form.populate_obj(user)
            if AppUser.query.filter_by(username=user.username).first() is not None:
                error += f"Username {user.username} existiert schon! "
            if AppUser.query.filter_by(email=user.email).first() is not None:
                error += f"Email {user.email} schon in Gebrauch! "
            if user.password in blacklist:
                error += "Dein Passwort ist zu simpel!"
            if not error:
                user.password = generate_password_hash(user.password)
                db.session.add(user)
                db.session.commit()
                session.clear()  # log user in
                session["user_id"] = user.id
                flash(f"{user.username}  registriert.", "success")
                logging.info(f"{user.username}  registered")
                return redirect(url_for("people.add_new_member"))
            else:
                logging.warning(f"{error}")
                flash(error.strip(), "danger")
        return render_template("auth/register.html", form=form)
    return redirect(url_for("auth.access"))


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    form = LoginForm()
    if form.validate_on_submit():
        error = None
        user = AppUser.query.filter_by(username=form.username.data).first()
        if not user:
            error = "Unknown username."
        elif not check_password_hash(user.password, form.password.data):
            error = f"Incorrect password for {user.username} ."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("people.index"))

        flash(error, "danger")
    return render_template("auth/login.html")


@bp.route("/users")
@login_required
def users():
    usrs = AppUser.query.all()
    return render_template("auth/users.html", users=usrs)


@bp.route("/users/edit/<userid>", methods=("GET", "POST"))
@login_required
def edit_user(userid):
    user = AppUser.query.filter_by(id=userid).first()
    if request.method == "POST":
        pw = request.form["password"]
        blacklist = open("static/blacklist.txt", "r").readlines()
        if pw not in blacklist:
            d = dict(admin=False)
            d["username"] = request.form["username"]
            d["password"] = generate_password_hash()
            d["email"] = request.form["email"]
            if request.form.get("admin"):
                d["admin"] = True
            _ = AppUser.query.filter_by(id=userid).update(d)
            _ = Member.query.filter_by(id=userid).update({"email": d["email"]})
            db.session.commit()

            flash(f"User '{d['username']}' updated", "success")
            return redirect(url_for("auth.users"))
        else:
            flash(f"Passwort zu simpel!", "danger")

    return render_template("auth/edit.html", user=user)


@bp.route("/users/delete/<userid>", methods=("GET",))
@login_required
def delete_user(userid):
    member = Member.query.filter_by(id=userid).first()
    user = AppUser.query.filter_by(id=userid).first()
    db.session.delete(member)
    db.session.commit()
    db.session.delete(user)
    db.session.commit()

    flash(f"User '{user.username}' with profile '{member.scoutname}' deleted", "warning")

    return redirect(url_for("auth.users"))


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))


@bp.errorhandler(429)
def ratelimit_handler(e):
    return "You have exceeded your rate limit!", 429
