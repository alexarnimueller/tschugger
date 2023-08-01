import os
from collections import OrderedDict
from flask import Blueprint
from flask import render_template, url_for
from datetime import date
from auth import login_required
from models import Member

bp = Blueprint("views", __name__)


@bp.context_processor
def inject_today_date():
    return {"today_date": date.today()}


@bp.route("/", methods=("GET",))
def index():
    imgs = os.listdir(url_for("static"))
    return render_template("tschugger.html", imgs=imgs)


@bp.route("/dashboard", methods=("GET", "POST"))
@login_required
def dashboard():
    # member data
    members_in = Member.query.all()
    years = {m.joined.year: 0 for m in members_in}
    for m in members_in:
        years[m.joined.year] += 1
    years = OrderedDict(sorted(years.items()))
    members = [
        {"name": f"{m.firstname} {m.lastname}", "url": f"/people/{m.id}", "lat": m.lat, "lon": m.lon}
        for m in members_in
        if isinstance(m.lat, float)
    ]

    # payments data
    catdict = {m.category: 0 for m in members_in}
    for m in members_in:
        catdict[m.category] += 1
    categories = list(catdict.keys())
    category_nums = list(catdict.values())

    return render_template(
        "dashboard.html",
        members=members,
        member_years=list(years.keys()),
        member_nums=list(years.values()),
        categories=categories,
        category_nums=category_nums,
    )
