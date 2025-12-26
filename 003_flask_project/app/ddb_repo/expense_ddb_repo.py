import boto3
import uuid
from datetime import datetime

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "ExpenseSplitApp"


class ExpenseRepositoryDDB:

    @staticmethod
    def create(description, amount, group_id, paid_by, splits=None):
        expense_id = str(uuid.uuid4())
        created_at = int(datetime.utcnow().timestamp())

        from app.ddb_repo.user_ddb_repo import UserRepositoryDDB
        from app.ddb_repo.group_ddb_repo import GroupRepositoryDDB

        payer = UserRepositoryDDB.get_by_id(paid_by)
        if not payer:
            raise ValueError("Payer user not found")

        if splits is None:
            group = GroupRepositoryDDB.get_by_id(group_id)
            if not group:
                raise ValueError("Group not found")

            member_count = len(group.get("members", []))
            if member_count == 0:
                raise ValueError("Group has no members")

            split_amount = amount / member_count
            splits = {member["user_id"]: split_amount for member in group["members"]}

        splits_list = []
        for user_id, split_amount in splits.items():
            user = UserRepositoryDDB.get_by_id(user_id)
            if user:
                splits_list.append(
                    {
                        "M": {
                            "user_id": {"S": user_id},
                            "name": {"S": user.name},
                            "username": {"S": user.username},
                            "amount": {"N": str(split_amount)},
                        }
                    }
                )

        try:
            dynamodb.put_item(
                TableName=TABLE_NAME,
                Item={
                    "PK": {"S": f"GROUP#{group_id}"},
                    "SK": {"S": f"EXPENSE#{created_at}#{expense_id}"},
                    "expense_id": {"S": expense_id},
                    "description": {"S": description},
                    "amount": {"N": str(amount)},
                    "paid_by": {
                        "M": {
                            "id": {"S": paid_by},
                            "name": {"S": payer.name},
                            "username": {"S": payer.username},
                        }
                    },
                    "splits": {"L": splits_list},
                    "expense_date": {"N": str(created_at)},
                    "created_at": {"N": str(created_at)},
                },
                ConditionExpression="attribute_not_exists(PK) OR attribute_not_exists(SK)",
            )

            return {
                "id": expense_id,
                "description": description,
                "amount": amount,
                "group_id": group_id,
                "paid_by": paid_by,
                "expense_date": created_at,
            }

        except dynamodb.exceptions.ConditionalCheckFailedException:
            raise ValueError("Expense already exists")

    @staticmethod
    def get_by_group(group_id):
        all_expenses = []
        last_evaluated_key = None

        while True:
            query_params = {
                "TableName": TABLE_NAME,
                "KeyConditionExpression": "PK = :pk AND begins_with(SK, :sk_prefix)",
                "ExpressionAttributeValues": {
                    ":pk": {"S": f"GROUP#{group_id}"},
                    ":sk_prefix": {"S": "EXPENSE#"},
                },
                "ScanIndexForward": False,
            }

            if last_evaluated_key:
                query_params["ExclusiveStartKey"] = last_evaluated_key

            response = dynamodb.query(**query_params)

            for item in response.get("Items", []):
                paid_by_map = item["paid_by"]["M"]

                splits = []
                if "splits" in item and "L" in item["splits"]:
                    for split_item in item["splits"]["L"]:
                        split_map = split_item["M"]
                        splits.append(
                            {
                                "user_id": split_map["user_id"]["S"],
                                "name": split_map["name"]["S"],
                                "username": split_map["username"]["S"],
                                "amount": float(split_map["amount"]["N"]),
                            }
                        )

                all_expenses.append(
                    {
                        "id": item["expense_id"]["S"],
                        "description": item["description"]["S"],
                        "amount": float(item["amount"]["N"]),
                        "group_id": group_id,
                        "paid_by": paid_by_map["id"]["S"],
                        "expense_date": int(item["expense_date"]["N"]),
                        "paid_by_user": {
                            "id": paid_by_map["id"]["S"],
                            "name": paid_by_map["name"]["S"],
                            "username": paid_by_map["username"]["S"],
                            "email": "",
                        },
                        "splits": splits,
                    }
                )

            last_evaluated_key = response.get("LastEvaluatedKey")
            if not last_evaluated_key:
                break

        return all_expenses

    @staticmethod
    def delete(expense_id, group_id):
        response = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression="PK = :pk AND begins_with(SK, :sk_prefix)",
            FilterExpression="expense_id = :expense_id",
            ExpressionAttributeValues={
                ":pk": {"S": f"GROUP#{group_id}"},
                ":sk_prefix": {"S": "EXPENSE#"},
                ":expense_id": {"S": expense_id},
            },
        )

        items = response.get("Items", [])
        if not items:
            return False

        item = items[0]
        try:
            dynamodb.delete_item(
                TableName=TABLE_NAME, Key={"PK": item["PK"], "SK": item["SK"]}
            )
            return True
        except Exception:
            return False

    @staticmethod
    def get_splits(expense_id, group_id):
        response = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression="PK = :pk AND begins_with(SK, :sk_prefix)",
            FilterExpression="expense_id = :expense_id",
            ExpressionAttributeValues={
                ":pk": {"S": f"GROUP#{group_id}"},
                ":sk_prefix": {"S": "EXPENSE#"},
                ":expense_id": {"S": expense_id},
            },
        )

        items = response.get("Items", [])
        if not items:
            return []

        item = items[0]
        splits = []

        if "splits" in item and "L" in item["splits"]:
            for split_item in item["splits"]["L"]:
                split_map = split_item["M"]
                splits.append(
                    {
                        "id": f"{expense_id}#{split_map['user_id']['S']}",
                        "expense_id": expense_id,
                        "user_id": split_map["user_id"]["S"],
                        "amount": float(split_map["amount"]["N"]),
                    }
                )

        return splits

    @staticmethod
    def get_by_id(expense_id, group_id=None):
        if group_id is None:
            raise ValueError("group_id is required for DynamoDB queries")

        response = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression="PK = :pk AND begins_with(SK, :sk_prefix)",
            FilterExpression="expense_id = :expense_id",
            ExpressionAttributeValues={
                ":pk": {"S": f"GROUP#{group_id}"},
                ":sk_prefix": {"S": "EXPENSE#"},
                ":expense_id": {"S": expense_id},
            },
        )

        items = response.get("Items", [])
        if not items:
            return None

        item = items[0]
        paid_by_map = item["paid_by"]["M"]

        return {
            "id": item["expense_id"]["S"],
            "description": item["description"]["S"],
            "amount": float(item["amount"]["N"]),
            "group_id": group_id,
            "paid_by": paid_by_map["id"]["S"],
            "expense_date": int(item["expense_date"]["N"]),
        }
