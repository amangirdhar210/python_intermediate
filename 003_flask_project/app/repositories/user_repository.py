from app import get_db
from app.models.user import User
import bcrypt
import uuid


class UserRepository:

    @staticmethod
    def create(email, username, name, password):
        user_id = str(uuid.uuid4())
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (id, email, username, password_hash, name) VALUES (?, ?, ?, ?, ?)",
            (user_id, email, username, password_hash, name),
        )
        db.commit()

        return UserRepository.get_by_id(user_id)

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, email, username, password_hash, name, created_at FROM users WHERE id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        if row:
            return User(
                id=row[0],
                email=row[1],
                username=row[2],
                password_hash=row[3],
                name=row[4],
                created_at=row[5],
            )
        return None

    @staticmethod
    def get_by_email(email):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, email, username, password_hash, name, created_at FROM users WHERE email = ?",
            (email,),
        )
        row = cursor.fetchone()
        if row:
            return User(
                id=row[0],
                email=row[1],
                username=row[2],
                password_hash=row[3],
                name=row[4],
                created_at=row[5],
            )
        return None

    @staticmethod
    def get_by_username(username):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, email, username, password_hash, name, created_at FROM users WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()
        if row:
            return User(
                id=row[0],
                email=row[1],
                username=row[2],
                password_hash=row[3],
                name=row[4],
                created_at=row[5],
            )
        return None

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, email, username, password_hash, name, created_at FROM users"
        )
        rows = cursor.fetchall()
        return [
            User(
                id=row[0],
                email=row[1],
                username=row[2],
                password_hash=row[3],
                name=row[4],
                created_at=row[5],
            )
            for row in rows
        ]

    @staticmethod
    def search(query):
        db = get_db()
        cursor = db.cursor()
        search_pattern = f"%{query}%"
        cursor.execute(
            "SELECT id, email, username, password_hash, name, created_at FROM users WHERE username LIKE ? OR email LIKE ? OR name LIKE ?",
            (search_pattern, search_pattern, search_pattern),
        )
        rows = cursor.fetchall()
        return [
            User(
                id=row[0],
                email=row[1],
                username=row[2],
                password_hash=row[3],
                name=row[4],
                created_at=row[5],
            )
            for row in rows
        ]

    @staticmethod
    def check_password(user, password):
        return bcrypt.checkpw(
            password.encode("utf-8"), user.password_hash.encode("utf-8")
        )
