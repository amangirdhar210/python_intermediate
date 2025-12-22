from app.repositories.expense_repository import ExpenseRepository
from app.repositories.group_repository import GroupRepository


class ExpenseService:

    @staticmethod
    def create_expense(
        description, amount, group_id, paid_by, split_type="equal", custom_splits=None
    ):
        members = GroupRepository.get_members(group_id)
        member_ids = [m["user_id"] for m in members]

        if split_type == "equal":
            split_amount = round(amount / len(member_ids), 2)
            splits = {user_id: split_amount for user_id in member_ids}

            remaining = round(amount - (split_amount * len(member_ids)), 2)
            if remaining != 0:
                splits[member_ids[0]] += remaining
        else:
            splits = custom_splits

        return ExpenseRepository.create(description, amount, group_id, paid_by, splits)

    @staticmethod
    def get_group_expenses(group_id):
        return ExpenseRepository.get_by_group(group_id)

    @staticmethod
    def get_expense(expense_id):
        return ExpenseRepository.get_by_id(expense_id)

    @staticmethod
    def get_expense_splits(expense_id):
        return ExpenseRepository.get_splits(expense_id)
