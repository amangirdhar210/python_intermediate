from app.repositories.expense_repository import ExpenseRepository


class ExpenseService:

    @staticmethod
    def create_expense(description, amount, group_id, paid_by):
        return ExpenseRepository.create(description, amount, group_id, paid_by)

    @staticmethod
    def get_group_expenses(group_id):
        return ExpenseRepository.get_by_group(group_id)

    @staticmethod
    def get_expense(expense_id):
        return ExpenseRepository.get_by_id(expense_id)
