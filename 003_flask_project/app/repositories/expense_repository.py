from app import get_db
import uuid
import time


class ExpenseRepository:

    @staticmethod
    def create(description, amount, group_id, paid_by):
        expense_id = str(uuid.uuid4())
        current_time = int(time.time())

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO expenses (id, description, amount, group_id, paid_by, expense_date, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                expense_id,
                description,
                amount,
                group_id,
                paid_by,
                current_time,
                current_time,
            ),
        )
        db.commit()
        return ExpenseRepository.get_by_id(expense_id)

    @staticmethod
    def get_by_id(expense_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, description, amount, group_id, paid_by, expense_date FROM expenses WHERE id = ?",
            (expense_id,),
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "description": row[1],
                "amount": row[2],
                "group_id": row[3],
                "paid_by": row[4],
                "expense_date": row[5],
            }
        return None

    @staticmethod
    def get_by_group(group_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """SELECT e.id, e.description, e.amount, e.group_id, e.paid_by, e.expense_date,
                      u.id as user_id, u.name, u.username, u.email
               FROM expenses e
               JOIN users u ON e.paid_by = u.id
               WHERE e.group_id = ?
               ORDER BY e.expense_date DESC""",
            (group_id,),
        )
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "description": row[1],
                "amount": row[2],
                "group_id": row[3],
                "paid_by": row[4],
                "expense_date": row[5],
                "paid_by_user": {
                    "id": row[6],
                    "name": row[7],
                    "username": row[8],
                    "email": row[9],
                },
            }
            for row in rows
        ]

    @staticmethod
    def delete(expense_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        db.commit()
        return cursor.rowcount > 0
