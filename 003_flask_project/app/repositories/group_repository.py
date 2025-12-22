from app import get_db
import uuid


class GroupRepository:

    @staticmethod
    def create(name, created_by, description=None):
        group_id = str(uuid.uuid4())

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO groups (id, name, created_by, description) VALUES (?, ?, ?, ?)",
            (group_id, name, created_by, description),
        )

        member_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO group_members (id, group_id, user_id) VALUES (?, ?, ?)",
            (member_id, group_id, created_by),
        )

        db.commit()
        return GroupRepository.get_by_id(group_id)

    @staticmethod
    def get_by_id(group_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, name, description, created_by, created_at FROM groups WHERE id = ?",
            (group_id,),
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "created_by": row[3],
                "created_at": row[4],
            }
        return None

    @staticmethod
    def get_user_groups(user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """SELECT g.id, g.name, g.description, g.created_by, g.created_at 
               FROM groups g 
               JOIN group_members gm ON g.id = gm.group_id 
               WHERE gm.user_id = ?""",
            (user_id,),
        )
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "created_by": row[3],
                "created_at": row[4],
            }
            for row in rows
        ]

    @staticmethod
    def add_member(group_id, user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id FROM group_members WHERE group_id = ? AND user_id = ?",
            (group_id, user_id),
        )
        if cursor.fetchone():
            return False

        member_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO group_members (id, group_id, user_id) VALUES (?, ?, ?)",
            (member_id, group_id, user_id),
        )
        db.commit()
        return True

    @staticmethod
    def get_members(group_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """SELECT gm.id, gm.group_id, gm.user_id, gm.joined_at,
                      u.id as user_id, u.name, u.username, u.email
               FROM group_members gm
               JOIN users u ON gm.user_id = u.id
               WHERE gm.group_id = ?""",
            (group_id,),
        )
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "group_id": row[1],
                "user_id": row[2],
                "joined_at": row[3],
                "user": {
                    "id": row[4],
                    "name": row[5],
                    "username": row[6],
                    "email": row[7],
                },
            }
            for row in rows
        ]

    @staticmethod
    def is_member(group_id, user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id FROM group_members WHERE group_id = ? AND user_id = ?",
            (group_id, user_id),
        )
        return cursor.fetchone() is not None

    @staticmethod
    def delete(group_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM groups WHERE id = ?", (group_id,))
        db.commit()
        return cursor.rowcount > 0
