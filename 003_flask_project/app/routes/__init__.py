from app.routes.auth import auth_bp
from app.routes.groups import groups_bp
from app.routes.expenses import expenses_bp
from app.routes.settlements import settlements_bp
from app.routes.main import main_bp

__all__ = ["auth_bp", "groups_bp", "expenses_bp", "settlements_bp", "main_bp"]
