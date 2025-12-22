from flask import Flask, g
from flask_login import LoginManager
import sqlite3
import os

login_manager = LoginManager()


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("splitwise.db", detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect("splitwise.db")
    with open("app/schema.sql", "r") as f:
        db.executescript(f.read())
    db.commit()
    db.close()


def create_app(config_name="development"):
    app = Flask(__name__)

    from config import config

    app.config.from_object(config[config_name])

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."

    app.teardown_appcontext(close_db)

    from app.routes.auth import auth_bp
    from app.routes.groups import groups_bp
    from app.routes.expenses import expenses_bp
    from app.routes.settlements import settlements_bp
    from app.routes.main import main_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(groups_bp, url_prefix="/groups")
    app.register_blueprint(expenses_bp, url_prefix="/expenses")
    app.register_blueprint(settlements_bp, url_prefix="/settlements")
    app.register_blueprint(main_bp, url_prefix="/")

    with app.app_context():
        if not os.path.exists("splitwise.db"):
            init_db()

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.repositories.user_repository import UserRepository

    return UserRepository.get_by_id(user_id)
