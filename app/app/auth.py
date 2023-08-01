import functools

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
from forms import UserRegistrationForm
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


@bp.route("/register", methods=("GET", "POST"))
def register():
    error = ""
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user = AppUser()
        form.populate_obj(user)
        if AppUser.query.filter_by(username=user.username).first() is not None:
            error += f"User existiert schon! "
        if AppUser.query.filter_by(email=user.email).first() is not None:
            error += f"Email schon in gebrauch!"
        if not error:
            user.password = generate_password_hash(user.password)
            db.session.add(user)
            db.session.commit()
            flash(f"{user.username}  registriert.", "success")
            return redirect(url_for("people.index"))
        else:
            flash(error, "error")
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        user = AppUser.query.filter_by(username=username).first()
        if not user:
            error = "Unknown username."
        elif not check_password_hash(user.password, password):
            error = f"Incorrect password for {user.username} ."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index"))

        flash(error, "error")
    return render_template("auth/login.html")


@bp.route("/users")
@login_required
def users():
    usrs = AppUser.query.all()
    return render_template("auth/users.html", users=usrs)


@bp.route("/users/edit/<userid>", methods=("GET", "POST"))
@login_required
def edit_user(userid):
    usr = AppUser.query.filter_by(id=userid).first()
    if request.method == "POST":
        d = dict()
        d["username"] = request.form["username"]
        d["password"] = generate_password_hash(request.form["password"])
        d["email"] = request.form["email"]
        _ = Member.query.filter_by(id=userid).update(d)
        db.session.commit()

        flash(f"User '{d['username']}' updated", "success")

        return redirect(url_for("auth.users"))

    return render_template("auth/edit.html", user=usr)


@bp.route("/users/delete/<userid>", methods=("GET",))
@login_required
def delete_user(userid):
    usr = AppUser.query.filter_by(id=userid).first()
    db.session.delete(usr)
    db.session.commit()

    flash(f"User '{usr.username}' deleted", "success")

    return redirect(url_for("auth.users"))


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))


@bp.errorhandler(429)
def ratelimit_handler(e):
    return "You have exceeded your rate limit!", 429
