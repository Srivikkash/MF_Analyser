from flask import Blueprint, jsonify, render_template, request
from app.services.fund_service import FundService

funds_bp = Blueprint("funds", __name__)


@funds_bp.route("/")
def listing():
    service = FundService()
    q = request.args.get("q", "")
    funds = service.search(q) if q else service.list_funds()
    return render_template("funds/list.html", funds=funds, q=q)


@funds_bp.route("/<scheme_code>")
def detail(scheme_code):
    service = FundService()
    detail = service.fund_detail(scheme_code)
    analytics = service.analytics(scheme_code)
    return render_template("funds/detail.html", detail=detail, analytics=analytics, scheme_code=scheme_code)


@funds_bp.route("/<scheme_code>/analytics")
def analytics_api(scheme_code):
    return jsonify(FundService().analytics(scheme_code))
