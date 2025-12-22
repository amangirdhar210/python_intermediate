from app.repositories.user_repository import UserRepository
from flask_login import login_user, logout_user


class AuthService:

    @staticmethod
    def register(email, username, name, password):
        if UserRepository.get_by_email(email):
            return None, "Email already exists"

        if UserRepository.get_by_username(username):
            return None, "Username already exists"

        user = UserRepository.create(email, username, name, password)
        return user, None

    @staticmethod
    def login(email_or_username, password):
        user = UserRepository.get_by_email(email_or_username)
        if not user:
            user = UserRepository.get_by_username(email_or_username)

        if user and UserRepository.check_password(user, password):
            login_user(user, remember=True)
            return user, None

        return None, "Invalid credentials"

    @staticmethod
    def logout():
        logout_user()
