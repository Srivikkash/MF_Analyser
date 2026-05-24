from flask import Blueprint, render_template
from app.services.fund_service import FundService

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def dashboard():
    service = FundService()
    funds = service.list_funds()[:20]
    return render_template("main/dashboard.html", funds=funds)
