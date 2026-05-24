from datetime import datetime

from bson import ObjectId
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import login_manager, mongo_db


class User(UserMixin):
    def __init__(self, data):
        self.data = data
        self.id = str(data["_id"])
        self.email = data["email"]
        self.name = data["name"]
        self.password_hash = data["password_hash"]

    @staticmethod
    def collection():
        return mongo_db.users

    @staticmethod
    def create(email, name, password):
        doc = {
            "email": email,
            "name": name,
            "password_hash": generate_password_hash(password),
            "created_at": datetime.utcnow(),
        }
        inserted = User.collection().insert_one(doc)
        doc["_id"] = inserted.inserted_id
        return User(doc)

    @staticmethod
    def find_by_email(email):
        doc = User.collection().find_one({"email": email})
        return User(doc) if doc else None

    @staticmethod
    def get_by_id(user_id):
        doc = User.collection().find_one({"_id": ObjectId(user_id)})
        return User(doc) if doc else None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get_by_id(user_id)
    except Exception:
        return None


class Watchlist:
    @staticmethod
    def collection():
        return mongo_db.watchlists

    @staticmethod
    def add(user_id, scheme_code, scheme_name):
        Watchlist.collection().insert_one(
            {
                "user_id": user_id,
                "scheme_code": scheme_code,
                "scheme_name": scheme_name,
                "created_at": datetime.utcnow(),
            }
        )


class PortfolioTransaction:
    @staticmethod
    def collection():
        return mongo_db.portfolio_transactions

    @staticmethod
    def add(user_id, scheme_code, scheme_name, amount, units, nav_at_purchase, txn_date):
        PortfolioTransaction.collection().insert_one(
            {
                "user_id": user_id,
                "scheme_code": scheme_code,
                "scheme_name": scheme_name,
                "amount": amount,
                "units": units,
                "nav_at_purchase": nav_at_purchase,
                "txn_date": txn_date,
                "created_at": datetime.utcnow(),
            }
        )

    @staticmethod
    def by_user(user_id):
        return list(PortfolioTransaction.collection().find({"user_id": user_id}).sort("txn_date", 1))
