import boto3
import uuid
from datetime import datetime

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "ExpenseSplitApp"


class SettlementRepositoryDDB:

    @staticmethod
    def create(group_id, from_user_id, to_user_id, amount):
        settlement_id = str(uuid.uuid4())
        settled_at = int(datetime.utcnow().timestamp())

        from app.ddb_repo.user_ddb_repo import UserRepositoryDDB

        from_user = UserRepositoryDDB.get_by_id(from_user_id)
        to_user = UserRepositoryDDB.get_by_id(to_user_id)

        if not from_user or not to_user:
            raise ValueError("User not found")

        try:
            dynamodb.put_item(
                TableName=TABLE_NAME,
                Item={
                    "PK": {"S": f"GROUP#{group_id}"},
                    "SK": {"S": f"SETTLEMENT#{settled_at}#{settlement_id}"},
                    "settlement_id": {"S": settlement_id},
                    "from_user": {
                        "M": {
                            "id": {"S": from_user_id},
                            "name": {"S": from_user.name},
                            "username": {"S": from_user.username},
                        }
                    },
                    "to_user": {
                        "M": {
                            "id": {"S": to_user_id},
                            "name": {"S": to_user.name},
                            "username": {"S": to_user.username},
                        }
                    },
                    "amount": {"N": str(amount)},
                    "settled_at": {"N": str(settled_at)},
                },
                ConditionExpression="attribute_not_exists(PK) OR attribute_not_exists(SK)",
            )

            return {
                "id": settlement_id,
                "group_id": group_id,
                "from_user_id": from_user_id,
                "to_user_id": to_user_id,
                "amount": amount,
                "settled_at": settled_at,
            }

        except dynamodb.exceptions.ConditionalCheckFailedException:
            raise ValueError("Settlement already exists")

    @staticmethod
    def get_by_group(group_id):
        all_settlements = []
        last_evaluated_key = None

        while True:
            query_params = {
                "TableName": TABLE_NAME,
                "KeyConditionExpression": "PK = :pk AND begins_with(SK, :sk_prefix)",
                "ExpressionAttributeValues": {
                    ":pk": {"S": f"GROUP#{group_id}"},
                    ":sk_prefix": {"S": "SETTLEMENT#"},
                },
                "ScanIndexForward": False,
            }

            if last_evaluated_key:
                query_params["ExclusiveStartKey"] = last_evaluated_key

            response = dynamodb.query(**query_params)

            for item in response.get("Items", []):
                from_user_map = item["from_user"]["M"]
                to_user_map = item["to_user"]["M"]

                all_settlements.append(
                    {
                        "id": item["settlement_id"]["S"],
                        "group_id": group_id,
                        "from_user_id": from_user_map["id"]["S"],
                        "to_user_id": to_user_map["id"]["S"],
                        "amount": float(item["amount"]["N"]),
                        "settled_at": int(item["settled_at"]["N"]),
                        "from_user": {
                            "id": from_user_map["id"]["S"],
                            "name": from_user_map["name"]["S"],
                            "username": from_user_map["username"]["S"],
                        },
                        "to_user": {
                            "id": to_user_map["id"]["S"],
                            "name": to_user_map["name"]["S"],
                            "username": to_user_map["username"]["S"],
                        },
                    }
                )

            last_evaluated_key = response.get("LastEvaluatedKey")
            if not last_evaluated_key:
                break

        return all_settlements

    @staticmethod
    def get_by_id(settlement_id, group_id):
        response = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression="PK = :pk AND begins_with(SK, :sk_prefix)",
            FilterExpression="settlement_id = :settlement_id",
            ExpressionAttributeValues={
                ":pk": {"S": f"GROUP#{group_id}"},
                ":sk_prefix": {"S": "SETTLEMENT#"},
                ":settlement_id": {"S": settlement_id},
            },
        )

        items = response.get("Items", [])
        if not items:
            return None

        item = items[0]
        from_user_map = item["from_user"]["M"]
        to_user_map = item["to_user"]["M"]

        return {
            "id": settlement_id,
            "group_id": group_id,
            "from_user_id": from_user_map["id"]["S"],
            "to_user_id": to_user_map["id"]["S"],
            "amount": float(item["amount"]["N"]),
            "settled_at": int(item["settled_at"]["N"]),
        }
