from flask import Blueprint, jsonify, request
from app.services.fund_service import FundService

api_bp = Blueprint("api", __name__)


@api_bp.route("/search")
def search():
    return jsonify(FundService().search(request.args.get("q", "")))
