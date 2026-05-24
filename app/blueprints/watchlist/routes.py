from flask import Blueprint, flash, redirect, url_for
from flask_login import current_user, login_required

from app.models import Watchlist

watchlist_bp = Blueprint("watchlist", __name__)


@watchlist_bp.route("/add/<scheme_code>/<path:scheme_name>")
@login_required
def add(scheme_code, scheme_name):
    Watchlist.add(current_user.id, scheme_code, scheme_name)
    flash("Added to watchlist", "success")
    return redirect(url_for("funds.detail", scheme_code=scheme_code))
