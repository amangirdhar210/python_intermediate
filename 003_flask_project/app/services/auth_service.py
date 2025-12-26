from app.ddb_repo.user_ddb_repo import UserRepositoryDDB
from flask_login import login_user, logout_user


class AuthService:

    @staticmethod
    def register(email, username, name, password):
        if UserRepositoryDDB.get_by_username(username):
            return None, "Username already exists"

        user = UserRepositoryDDB.create(email, username, name, password)
        return user, None

    @staticmethod
    def login(username, password):
        user = UserRepositoryDDB.get_by_username(username)

        if user and UserRepositoryDDB.check_password(user, password):
            login_user(user, remember=True)
            return user, None

        return None, "Invalid credentials"

    @staticmethod
    def logout():
        logout_user()
