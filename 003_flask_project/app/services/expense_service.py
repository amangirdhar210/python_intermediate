from app.ddb_repo.expense_ddb_repo import ExpenseRepositoryDDB


class ExpenseService:

    @staticmethod
    def create_expense(description, amount, group_id, paid_by):
        return ExpenseRepositoryDDB.create(description, amount, group_id, paid_by)

    @staticmethod
    def get_group_expenses(group_id):
        return ExpenseRepositoryDDB.get_by_group(group_id)

    @staticmethod
    def get_expense(expense_id):
        return ExpenseRepositoryDDB.get_by_id(expense_id)
