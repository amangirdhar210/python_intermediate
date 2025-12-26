from app.ddb_repo.expense_ddb_repo import ExpenseRepositoryDDB
from app.ddb_repo.settlement_ddb_repo import SettlementRepositoryDDB
from app.ddb_repo.user_ddb_repo import UserRepositoryDDB
from app.ddb_repo.group_ddb_repo import GroupRepositoryDDB


class BalanceService:

    @staticmethod
    def calculate_balances(group_id):
        expenses = ExpenseRepositoryDDB.get_by_group(group_id)
        settlements = SettlementRepositoryDDB.get_by_group(group_id)
        members = GroupRepositoryDDB.get_members(group_id)
        member_ids = [m["user_id"] for m in members]

        balances = {}

        for expense in expenses:
            split_amount = expense["amount"] / len(member_ids)

            for user_id in member_ids:
                if user_id != expense["paid_by"]:
                    key = (user_id, expense["paid_by"])
                    if key not in balances:
                        balances[key] = 0
                    balances[key] += split_amount

        for settlement in settlements:
            key = (settlement["from_user_id"], settlement["to_user_id"])
            if key in balances:
                balances[key] -= settlement["amount"]

        result = []
        for (from_user_id, to_user_id), amount in balances.items():
            if amount > 0.01:
                from_user = UserRepositoryDDB.get_by_id(from_user_id)
                to_user = UserRepositoryDDB.get_by_id(to_user_id)

                result.append(
                    {
                        "from_user_id": from_user_id,
                        "to_user_id": to_user_id,
                        "amount": round(amount, 2),
                        "from_user": {
                            "id": from_user.id,
                            "name": from_user.name,
                            "username": from_user.username,
                            "email": from_user.email,
                        },
                        "to_user": {
                            "id": to_user.id,
                            "name": to_user.name,
                            "username": to_user.username,
                            "email": to_user.email,
                        },
                    }
                )

        return result

    @staticmethod
    def settle_up(group_id, from_user_id, to_user_id, amount):
        return SettlementRepositoryDDB.create(
            group_id, from_user_id, to_user_id, amount
        )

    @staticmethod
    def get_user_balance_summary(user_id, group_id):
        balances = BalanceService.calculate_balances(group_id)

        owes = []
        owed = []

        for balance in balances:
            if balance["from_user_id"] == user_id:
                owes.append(balance)
            elif balance["to_user_id"] == user_id:
                owed.append(balance)

        return {"owes": owes, "owed": owed}
