from app import get_db
import uuid


class SettlementRepository:

    @staticmethod
    def create(group_id, from_user_id, to_user_id, amount):
        settlement_id = str(uuid.uuid4())

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO settlements (id, group_id, from_user_id, to_user_id, amount) VALUES (?, ?, ?, ?, ?)",
            (settlement_id, group_id, from_user_id, to_user_id, amount),
        )
        db.commit()

        return SettlementRepository.get_by_id(settlement_id)

    @staticmethod
    def get_by_id(settlement_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, group_id, from_user_id, to_user_id, amount, settled_at FROM settlements WHERE id = ?",
            (settlement_id,),
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "group_id": row[1],
                "from_user_id": row[2],
                "to_user_id": row[3],
                "amount": row[4],
                "settled_at": row[5],
            }
        return None

    @staticmethod
    def get_by_group(group_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, group_id, from_user_id, to_user_id, amount, settled_at FROM settlements WHERE group_id = ? ORDER BY settled_at DESC",
            (group_id,),
        )
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "group_id": row[1],
                "from_user_id": row[2],
                "to_user_id": row[3],
                "amount": row[4],
                "settled_at": row[5],
            }
            for row in rows
        ]

    @staticmethod
    def get_by_user(user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, group_id, from_user_id, to_user_id, amount, settled_at FROM settlements WHERE from_user_id = ? OR to_user_id = ? ORDER BY settled_at DESC",
            (user_id, user_id),
        )
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "group_id": row[1],
                "from_user_id": row[2],
                "to_user_id": row[3],
                "amount": row[4],
                "settled_at": row[5],
            }
            for row in rows
        ]
