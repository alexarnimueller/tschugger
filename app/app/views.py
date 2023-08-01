from flask import Blueprint
from flask import render_template
from datetime import date

bp = Blueprint("views", __name__)


@bp.context_processor
def inject_today_date():
    return {"today_date": date.today()}


@bp.route("/", methods=("GET",))
def index():
    return render_template("index.html")
