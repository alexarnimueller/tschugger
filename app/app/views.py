from flask import Blueprint
from flask import render_template

bp = Blueprint("views", __name__)


@bp.route("/", methods=("GET",))
def index():
    return render_template("index.html")
