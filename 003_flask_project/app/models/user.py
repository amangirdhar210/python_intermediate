from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, email, username, password_hash, name, created_at):
        self.id = id
        self.email = email
        self.username = username
        self.password_hash = password_hash
        self.name = name
        self.created_at = created_at

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
