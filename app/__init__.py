from flask import Flask
from flask_caching import Cache
from flask_login import LoginManager
from pymongo import MongoClient

from config import Config

login_manager = LoginManager()
cache = Cache()
mongo_client = None
mongo_db = None


def create_app(config_class=Config):
    global mongo_client, mongo_db

    app = Flask(__name__)
    app.config.from_object(config_class)

    login_manager.init_app(app)
    cache.init_app(app)

    mongo_client = MongoClient(app.config["MONGO_URI"])
    mongo_db = mongo_client[app.config["MONGO_DB_NAME"]]

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.main.routes import main_bp
    from app.blueprints.funds.routes import funds_bp
    from app.blueprints.portfolio.routes import portfolio_bp
    from app.blueprints.watchlist.routes import watchlist_bp
    from app.blueprints.api.routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(funds_bp, url_prefix="/funds")
    app.register_blueprint(portfolio_bp, url_prefix="/portfolio")
    app.register_blueprint(watchlist_bp, url_prefix="/watchlist")
    app.register_blueprint(api_bp, url_prefix="/api")

    from app.utils.errors import register_error_handlers
    register_error_handlers(app)

    return app
