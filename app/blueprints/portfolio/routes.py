from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.models import PortfolioTransaction
from app.services.fund_service import FundService

portfolio_bp = Blueprint("portfolio", __name__)


@portfolio_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        PortfolioTransaction.add(
            user_id=current_user.id,
            scheme_code=request.form["scheme_code"],
            scheme_name=request.form["scheme_name"],
            amount=float(request.form["amount"]),
            units=float(request.form["units"]),
            nav_at_purchase=float(request.form["nav"]),
            txn_date=datetime.strptime(request.form["txn_date"], "%Y-%m-%d"),
        )
        flash("Transaction added", "success")
        return redirect(url_for("portfolio.index"))

    txns = PortfolioTransaction.by_user(current_user.id)
    service = FundService()
    enriched = []
    for t in txns:
        nav = service.analytics(t["scheme_code"]).get("latest_nav", t["nav_at_purchase"])
        enriched.append({
            "scheme_name": t["scheme_name"],
            "units": t["units"],
            "current": nav,
            "value": nav * t["units"],
        })
    return render_template("portfolio/index.html", rows=enriched)
