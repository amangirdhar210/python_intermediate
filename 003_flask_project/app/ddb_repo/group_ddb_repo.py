import boto3
import uuid
from datetime import datetime

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "ExpenseSplitApp"


class GroupRepositoryDDB:

    @staticmethod
    def create(name, created_by, description=None):
        group_id = str(uuid.uuid4())
        created_at = int(datetime.utcnow().timestamp())

        from app.ddb_repo.user_ddb_repo import UserRepositoryDDB

        creator = UserRepositoryDDB.get_by_id(created_by)
        if not creator:
            raise ValueError("Creator user not found")

        try:
            dynamodb.transact_write_items(
                TransactItems=[
                    {
                        "Put": {
                            "TableName": TABLE_NAME,
                            "Item": {
                                "PK": {"S": f"GROUP#{group_id}"},
                                "SK": {"S": "Group_Info"},
                                "name": {"S": name},
                                "description": {"S": description or ""},
                                "created_by": {"S": created_by},
                                "created_by_name": {"S": creator["name"]},
                                "created_at": {"N": str(created_at)},
                                "members": {
                                    "L": [
                                        {
                                            "M": {
                                                "user_id": {"S": created_by},
                                                "username": {"S": creator["username"]},
                                                "name": {"S": creator["name"]},
                                                "joined_at": {"N": str(created_at)},
                                            }
                                        }
                                    ]
                                },
                                "member_count": {"N": "1"},
                            },
                            "ConditionExpression": "attribute_not_exists(PK)",
                        }
                    },
                    {
                        "Put": {
                            "TableName": TABLE_NAME,
                            "Item": {
                                "PK": {"S": f"USER#{created_by}"},
                                "SK": {"S": f"GROUP#{group_id}"},
                                "group_id": {"S": group_id},
                                "group_name": {"S": name},
                                "description": {"S": description or ""},
                                "created_by": {"S": created_by},
                                "created_by_name": {"S": creator["name"]},
                                "joined_at": {"N": str(created_at)},
                            },
                        }
                    },
                ]
            )

            return GroupRepositoryDDB.get_by_id(group_id)

        except dynamodb.exceptions.TransactionCanceledException as e:
            raise ValueError("Failed to create group")

    @staticmethod
    def get_by_id(group_id):
        response = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression="PK = :pk AND SK = :sk",
            ExpressionAttributeValues={
                ":pk": {"S": f"GROUP#{group_id}"},
                ":sk": {"S": "Group_Info"},
            },
        )

        items = response.get("Items", [])
        if not items:
            return None

        item = items[0]

        members = []
        if "members" in item and "L" in item["members"]:
            for member_item in item["members"]["L"]:
                member_map = member_item["M"]
                members.append(
                    {
                        "user_id": member_map["user_id"]["S"],
                        "username": member_map["username"]["S"],
                        "name": member_map["name"]["S"],
                        "joined_at": int(member_map["joined_at"]["N"]),
                    }
                )

        return {
            "id": group_id,
            "name": item["name"]["S"],
            "description": item.get("description", {}).get("S", ""),
            "created_by": item["created_by"]["S"],
            "created_by_name": item["created_by_name"]["S"],
            "created_at": int(item["created_at"]["N"]),
            "members": members,
            "member_count": int(item.get("member_count", {}).get("N", "0")),
        }

    @staticmethod
    def get_user_groups(user_id):
        all_groups = []
        last_evaluated_key = None

        while True:
            query_params = {
                "TableName": TABLE_NAME,
                "KeyConditionExpression": "PK = :pk AND begins_with(SK, :sk_prefix)",
                "ExpressionAttributeValues": {
                    ":pk": {"S": f"USER#{user_id}"},
                    ":sk_prefix": {"S": "GROUP#"},
                },
            }

            if last_evaluated_key:
                query_params["ExclusiveStartKey"] = last_evaluated_key

            response = dynamodb.query(**query_params)

            for item in response.get("Items", []):
                all_groups.append(
                    {
                        "id": item["group_id"]["S"],
                        "name": item["group_name"]["S"],
                        "description": item.get("description", {}).get("S", ""),
                        "created_by": item["created_by"]["S"],
                        "created_by_name": item["created_by_name"]["S"],
                        "joined_at": int(item["joined_at"]["N"]),
                    }
                )

            last_evaluated_key = response.get("LastEvaluatedKey")
            if not last_evaluated_key:
                break

        return all_groups

    @staticmethod
    def add_member(group_id, user_id):
        from app.ddb_repo.user_ddb_repo import UserRepositoryDDB

        user = UserRepositoryDDB.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        group = GroupRepositoryDDB.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")

        if GroupRepositoryDDB.is_member(group_id, user_id):
            return False

        joined_at = int(datetime.utcnow().timestamp())

        new_member = {
            "M": {
                "user_id": {"S": user_id},
                "username": {"S": user["username"]},
                "name": {"S": user["name"]},
                "joined_at": {"N": str(joined_at)},
            }
        }

        try:
            dynamodb.transact_write_items(
                TransactItems=[
                    {
                        "Update": {
                            "TableName": TABLE_NAME,
                            "Key": {
                                "PK": {"S": f"GROUP#{group_id}"},
                                "SK": {"S": "Group_Info"},
                            },
                            "UpdateExpression": "SET members = list_append(members, :new_member), member_count = member_count + :inc",
                            "ExpressionAttributeValues": {
                                ":new_member": {"L": [new_member]},
                                ":inc": {"N": "1"},
                            },
                        }
                    },
                    {
                        "Put": {
                            "TableName": TABLE_NAME,
                            "Item": {
                                "PK": {"S": f"USER#{user_id}"},
                                "SK": {"S": f"GROUP#{group_id}"},
                                "group_id": {"S": group_id},
                                "group_name": {"S": group["name"]},
                                "description": {"S": group.get("description", "")},
                                "created_by": {"S": group["created_by"]},
                                "created_by_name": {"S": group["created_by_name"]},
                                "joined_at": {"N": str(joined_at)},
                            },
                            "ConditionExpression": "attribute_not_exists(PK) OR attribute_not_exists(SK)",
                        }
                    },
                ]
            )
            return True

        except dynamodb.exceptions.TransactionCanceledException:
            return False

    @staticmethod
    def get_members(group_id):
        group = GroupRepositoryDDB.get_by_id(group_id)
        if not group:
            return []

        members_list = []
        for member in group.get("members", []):
            members_list.append(
                {
                    "id": f"{group_id}#{member['user_id']}",
                    "group_id": group_id,
                    "user_id": member["user_id"],
                    "joined_at": member["joined_at"],
                    "user": {
                        "id": member["user_id"],
                        "name": member["name"],
                        "username": member["username"],
                        "email": "",
                    },
                }
            )

        return members_list

    @staticmethod
    def is_member(group_id, user_id):
        response = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression="PK = :pk AND SK = :sk",
            ExpressionAttributeValues={
                ":pk": {"S": f"USER#{user_id}"},
                ":sk": {"S": f"GROUP#{group_id}"},
            },
        )

        return len(response.get("Items", [])) > 0

    @staticmethod
    def delete_by_id(group_id):
        group = GroupRepositoryDDB.get_by_id(group_id)
        if not group:
            return False

        delete_items = [
            {
                "Delete": {
                    "TableName": TABLE_NAME,
                    "Key": {
                        "PK": {"S": f"GROUP#{group_id}"},
                        "SK": {"S": "Group_Info"},
                    },
                }
            }
        ]

        for member in group.get("members", []):
            delete_items.append(
                {
                    "Delete": {
                        "TableName": TABLE_NAME,
                        "Key": {
                            "PK": {"S": f'USER#{member["user_id"]}'},
                            "SK": {"S": f"GROUP#{group_id}"},
                        },
                    }
                }
            )

        expenses_response = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression="PK = :pk AND begins_with(SK, :sk_prefix)",
            ExpressionAttributeValues={
                ":pk": {"S": f"GROUP#{group_id}"},
                ":sk_prefix": {"S": "EXPENSE#"},
            },
        )

        for expense in expenses_response.get("Items", []):
            delete_items.append(
                {
                    "Delete": {
                        "TableName": TABLE_NAME,
                        "Key": {"PK": expense["PK"], "SK": expense["SK"]},
                    }
                }
            )

        settlements_response = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression="PK = :pk AND begins_with(SK, :sk_prefix)",
            ExpressionAttributeValues={
                ":pk": {"S": f"GROUP#{group_id}"},
                ":sk_prefix": {"S": "SETTLEMENT#"},
            },
        )

        for settlement in settlements_response.get("Items", []):
            delete_items.append(
                {
                    "Delete": {
                        "TableName": TABLE_NAME,
                        "Key": {"PK": settlement["PK"], "SK": settlement["SK"]},
                    }
                }
            )

        batch_size = 100
        for i in range(0, len(delete_items), batch_size):
            batch = delete_items[i : i + batch_size]
            try:
                dynamodb.transact_write_items(TransactItems=batch)
            except Exception as e:
                print(f"Error deleting batch: {e}")
                return False

        return True
