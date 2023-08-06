from flask import Blueprint
from flask import render_template
from auth import login_required

bp = Blueprint("views", __name__)


@bp.route("/", methods=("GET",))
def index():
    return render_template("index.html")


@bp.route("/infos", methods=("GET",))
@login_required
def infos():
    return render_template("infos.html")
