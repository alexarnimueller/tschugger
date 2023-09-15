import os
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from auth import login_required

bp = Blueprint("views", __name__)


@bp.route("/", methods=("GET",))
def index():
    return render_template("index.html")


@bp.route("/infos", methods=("GET",))
@login_required
def infos():
    return render_template("infos.html")


@bp.route("/ausbildung", methods=("GET",))
@login_required
def ausbildung():
    return render_template("ausbildung.html")


@bp.route("/hack", methods=("GET", "POST"))
def hack():
    if request.method == "POST":
        password = request.form["password"]
        if password == "raclette":
            session["hacked"] = True
            return redirect(url_for("views.valmira"))
    return render_template("hack.html")


@bp.route("/valmira", methods=("GET", "POST"))
def valmira():
    if session.get("hacked", False):
        if request.method == "POST":
            password = request.form["handy"]
            if os.getenv("VALMIRA_HANDY") == password:
                session["valmira"] = True
                return redirect(url_for("views.ortung"))

            flash("Nummer unbekannt!", "danger")
        return render_template("valmira.html")
    return redirect(url_for("views.hack"))


@bp.route("/ortung", methods=("GET",))
def ortung():
    if session.get("valmira", False):
        return render_template("ortung.html")
    return render_template("valmira.html")
