import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
import requests
import logging
from __init__ import db
from datetime import date, datetime
from models import Member
from auth import login_required
from sqlalchemy import not_

bp = Blueprint("people", __name__, url_prefix="/people")
logger = logging.getLogger(__name__)


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    """Show all the members in alphabetical order by lastname"""
    if request.method == "POST":
        firstname = "%" + request.form["inputName"] + "%"
        lastname = "%" + request.form["inputLastName"] + "%"
        email = "%" + request.form["inputEmail"] + "%"
        category = sorted(request.form.getlist("inputCategory"))
        medium = "%" + request.form["inputMedium"] + "%"
        country = "%" + request.form["inputCountry"] + "%"
        active = [True] if request.form.get("activeCheck") else [True, False]
        afterdate = request.form["afterDate"] if request.form["afterDate"] else "2010-01-01"
        befordate = request.form["beforeDate"] if request.form["beforeDate"] else date.today().strftime("%Y-%m-%d")
        members = Member.query.filter(
            Member.firstname.like(firstname),
            Member.lastname.like(lastname),
            (Member.email1.like(email) | Member.email2.like(email)),
            Member.joined.between(afterdate, befordate),
            Member.category.in_(category),
            Member.country.like(country),
            Member.medium.like(medium),
            Member.active.in_(active),
        ).all()
        srchstrng = firstname + " " + lastname + " " + email + " " + " " + medium + " " + country
        return render_template(
            "people/people.html",
            title=f"Search Result For \"{srchstrng.replace('%', '').strip()}\"",
            members=members,
            emails=";".join([m.email1 for m in members if m.email1]),
            emails_all=";".join([m.email1 for m in members if m.email1])
            + ";"
            + ";".join([m.email2 for m in members if m.email2]),
        )
    else:
        title = "Patrouille"
        members = Member.query.all()
        imgs = os.listdir("static/images")
        return render_template(
            "tschugger.html",
            title=title,
            members=members,
            imgs=imgs,
        )


@bp.route("/<memberid>", methods=("GET", "POST"))
@login_required
def get_member_details(memberid):
    """Get all member details by member id.

    :param memberid: member ID
    :return: a form containing all the member information
    :raise 404: if the member does not exist
    """
    pdf = ""
    if request.method == "POST":
        d = dict()
        d["title"] = request.form["title"]
        d["firstname"] = request.form["firstname"]
        d["lastname"] = request.form["lastname"]
        d["email1"] = request.form["email1"]
        d["email2"] = request.form["email2"]
        d["phone"] = request.form["phone"]
        if request.form.get("active"):
            d["active"] = True
        else:
            d["active"] = False
        d["category"] = request.form["category"]
        d["medium"] = request.form["medium"]
        d["notes"] = request.form["notes"]

        d["addr1"] = request.form["addr1"]
        d["addr2"] = request.form["addr2"]
        d["addr3"] = request.form["addr3"]
        d["city"] = request.form["city"]
        d["zipcode"] = request.form["zipcode"]
        d["country"] = request.form["country"]
        d["joined"] = datetime.fromisoformat(request.form["joined"])
        # d["pdf"] = request.file["country"].read()
        pdf = "testfile.pdf"
        _ = Member.query.filter_by(id=memberid).update(d)
        db.session.commit()
        flash(f"Member {d['firstname']} {d['lastname']} updated")

    memberdetails = Member.query.filter_by(id=memberid).first()

    return render_template(
        "people/member.html",
        member=memberdetails,
        pdf=pdf,
    )


@bp.route("/add", methods=("GET", "POST"))
@login_required
def add_new_member():
    """Add a new member to the DB"""
    if request.method == "POST":
        d, ad = dict(), dict()
        d["email1"] = request.form["email1"]
        d["email2"] = request.form["email2"]
        rslt1 = Member.query.filter_by(email1=d["email1"]).first()
        rslt2 = Member.query.filter_by(email1=d["email2"]).first()
        if rslt1:
            flash(f"Email address '{d['email1']}' already exists in the database!")
        elif rslt2:
            flash(f"Email address '{d['email2']}' already exists in the database!")
        else:
            last_member = Member.query.order_by(Member.id.desc()).first()
            d["id"] = last_member.id + 1
            d["title"] = request.form["title"]
            d["firstname"] = request.form["firstname"]
            d["lastname"] = request.form["lastname"]
            d["phone"] = request.form["phone"]
            if request.form.get("active"):
                d["active"] = True
            else:
                d["active"] = False
            d["category"] = request.form["category"]
            d["medium"] = request.form.get("medium", "online")
            d["notes"] = request.form["notes"]
            d["addr1"] = request.form["addr1"]
            d["addr2"] = request.form["addr2"]
            d["addr3"] = request.form["addr3"]
            d["city"] = request.form["city"]
            d["zipcode"] = request.form["zipcode"]
            d["country"] = request.form["country"]
            d["joined"] = datetime.fromisoformat(request.form["joined"])

            record = Member(**d)
            db.session.add(record)
            db.session.commit()

            flash(f"New member {d['firstname']} {d['lastname']} created")

    return render_template("people/new.html")


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


@bp.route("/equinox", methods=("GET",))
@login_required
def equinox():
    # equinoxlist = Member.query.filter_by(equinox=True)
    right_category = Member.query.filter(not_(Member.category.like("%minus%")), Member.active).all()
    # members = list(set(list(equinoxlist) + list(right_category)))
    members = right_category
    return render_template(
        "people/people.html",
        title=f"Equinox List Members",
        members=members,
        emails=";".join([m.email1 for m in members if m.email1]),
        emails_all=";".join([m.email1 for m in members if m.email1])
        + ";"
        + ";".join([m.email2 for m in members if m.email2]),
    )


@bp.route("/delete_pdf/<memberid>", methods=("GET",))
@login_required
def delete_pdf(memberid):
    return redirect(url_for("people.get_member_details", memberid=memberid))


@bp.context_processor
def inject_today_date():
    return {"today_date": date.today()}


def address_to_coords(address_string: str):
    """Translate an address into lat and lon coordinates using the openstreetmap API."""
    apikey = os.getenv("GOOGLE_APIKEY")
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address_string}&key={apikey}"
    response = requests.get(url)
    data = response.json()
    try:
        rslt = data["results"][0]["geometry"]["location"]
        return [float(rslt["lat"]), float(rslt["lng"])]
    except IndexError:
        return [None, None]


def coords_for_members():
    """Translate the address to coordinates for all members which don't yet have them."""
    members = Member.query.all()
    for m in members:
        print(f"processing coordinates for {m} ...")
        if any([m.addr1, m.addr2, m.addr3, m.city]):
            address = f"{m.zipcode} {m.city}, {m.country}".replace("None", "").replace(", , ", ", ")
            lat, lon = address_to_coords(address)
            print(f"\tFound {lat:.4f} {lon:.4f}")
            m.lat, m.lon = lat, lon
            db.session.commit()
            if lat is None:
                print("\tNot found")
        else:
            print("\tNo address")
