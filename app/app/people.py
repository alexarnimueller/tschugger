import os
from random import choice
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import logging
from __init__ import db
from datetime import date
from models import Member, AppUser
from auth import login_required
from forms import ProfileForm

bp = Blueprint("people", __name__, url_prefix="/people")


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


@bp.route("/add", methods=("GET", "POST"))
@login_required
def add_new_member():
    user = AppUser.query.filter_by(id=session["user_id"]).first()
    logging.info(f"found {user} logged in")
    form = ProfileForm(email=user.email)
    logging.info(form)
    if form.validate_on_submit():
        logging.info(f"new member form validated")
        members = Member.query.all()
        imgs = set(os.listdir("static/images")).difference(set([m.img for m in members]))
        member = Member()
        form.populate_obj(member)
        member.id = user.id
        member.img = choice(list(imgs))  # randomly choose image not yet used
        db.session.add(member)
        db.session.commit()
        flash(f"Ahoi Tschugger '{member.scoutname}'!", "success")
        logging.info(f"Tschugger {member.scoutname} updated")
        return redirect(url_for("people.index"))

    return render_template("member.html", form=form, change=True)


@bp.route("/<memberid>", methods=("GET", "POST"))
@login_required
def get_member_details(memberid):
    """Get all member details by member id.

    :param memberid: member ID
    :return: a form containing all the member information
    :raise 404: if the member does not exist
    """
    change = False
    member = Member.query.filter_by(id=memberid).first()
    logging.info(member)
    form = ProfileForm(obj=member)
    if memberid == session["user_id"]:
        logging.info("member allowed to change info")
        change = True
        if form.validate_on_submit():
            logging.info("form validated successfully")
            members = Member.query.all()
            imgs = set(os.listdir("static/images")).difference(set([m.img for m in members]))
            form.populate_obj(member)
            member.img = choice(list(imgs))  # randomly choose image not yet used
            db.session.add(member)
            db.session.commit()
            flash(f"Profil von Tschugger '{member.scoutname}' angepasst!", "success")
            return redirect(url_for("people.index"))

    return render_template("member.html", form=form, change=change)


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
