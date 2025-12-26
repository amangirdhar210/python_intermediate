from flask import Flask
from flask_login import LoginManager
import os

login_manager = LoginManager()


def create_app(config_name="development"):
    app = Flask(__name__)

    from config import config

    app.config.from_object(config[config_name])

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."

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

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.ddb_repo.user_ddb_repo import UserRepositoryDDB

    return UserRepositoryDDB.get_by_id(user_id)
