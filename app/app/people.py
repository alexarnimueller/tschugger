from flask import Blueprint, render_template, request, flash, redirect, url_for
import logging
from __init__ import db
from datetime import date
from models import Member, AppUser
from auth import login_required

bp = Blueprint("people", __name__, url_prefix="/people")
logger = logging.getLogger(__name__)


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    title = "Patrouille"
    members = Member.query.all()
    return render_template(
        "tschugger.html",
        title=title,
        members=members,
    )


@bp.route("/<memberid>", methods=("GET", "POST"))
@login_required
def get_member_details(memberid):
    """Get all member details by member id.

    :param memberid: member ID
    :return: a form containing all the member information
    :raise 404: if the member does not exist
    """
    if request.method == "POST":
        d = dict()
        d["firstname"] = request.form["firstname"]
        d["lastname"] = request.form["lastname"]
        d["scoutname"] = request.form["scoutname"]
        d["email"] = request.form["email"]
        d["phone"] = request.form["phone"]
        d["notes"] = request.form["notes"]
        d["img"] = request.form["img"]
        _ = Member.query.filter_by(id=memberid).update(d)
        db.session.commit()
        flash(f"Tschugger {d['scoutname']} updated", "success")

    memberdetails = Member.query.filter_by(id=memberid).first()

    return render_template(
        "people/member.html",
        member=memberdetails,
    )


@bp.route("/add", methods=["POST"])
@login_required
def add():
    """Add a new member to the DB"""
    if "username" in request.form:  # coming from first registration
        details = {"id": request.form["id"], "email": request.form["email"]}
        return render_template("people/new.html", member=details)
    else:
        d = dict()
        d["id"] = request.form["id"]
        d["firstname"] = request.form["firstname"]
        d["lastname"] = request.form["lastname"]
        d["scoutname"] = request.form["scoutname"]
        d["email"] = request.form["email"]
        d["phone"] = request.form["phone"]
        d["notes"] = request.form["notes"]
        d["img"] = request.form["img"]
        record = Member(**d)
        db.session.add(record)
        db.session.commit()
        flash(f"New member {d['firstname']} {d['lastname']} created")
        return redirect("people.index")


@bp.route("/nomail", methods=("GET",))
@login_required
def nomail():
    nomailmembers = Member.query.filter_by(email1=None)
    return render_template("people/people.html", title=f"Members with no email address", members=nomailmembers)


@bp.route("/inactive", methods=("GET",))
@login_required
def inactive():
    inactivemembers = Member.query.filter_by(active=False)
    return render_template(
        "people/people.html",
        title=f"Inactive Members",
        members=inactivemembers,
        emails=";".join([m.email1 for m in inactivemembers if m.email1]),
        emails_all=";".join([m.email1 for m in inactivemembers if m.email1])
        + ";"
        + ";".join([m.email2 for m in inactivemembers if m.email2]),
    )


@bp.route("/delete_pdf/<memberid>", methods=("GET",))
@login_required
def delete_pdf(memberid):
    return redirect(url_for("people.get_member_details", memberid=memberid))


@bp.context_processor
def inject_today_date():
    return {"today_date": date.today()}
