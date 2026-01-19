import boto3
import bcrypt
import uuid
from decimal import Decimal
from datetime import datetime
from app.models.user import User

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "ExpenseSplitApp"


class UserRepositoryDDB:

    @staticmethod
    def create(email, username, name, password):
        user_id = str(uuid.uuid4())
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        created_at = int(datetime.utcnow().timestamp())

        try:
            dynamodb.transact_write_items(
                TransactItems=[
                    {
                        "Put": {
                            "TableName": TABLE_NAME,
                            "Item": {
                                "PK": {"S": f"USER#{user_id}"},
                                "SK": {"S": "PROFILE"},
                                "email": {"S": email},
                                "username": {"S": username},
                                "password_hash": {"S": password_hash},
                                "name": {"S": name},
                                "created_at": {"N": str(created_at)},
                            },
                            "ConditionExpression": "attribute_not_exists(PK)",
                        }
                    },
                    {
                        "Put": {
                            "TableName": TABLE_NAME,
                            "Item": {
                                "PK": {"S": f"USER#{username}"},
                                "SK": {"S": "PROFILE"},
                                "email": {"S": email},
                                "user_id": {"S": user_id},
                                "password_hash": {"S": password_hash},
                                "name": {"S": name},
                                "created_at": {"N": str(created_at)},
                            },
                            "ConditionExpression": "attribute_not_exists(PK)",
                        }
                    },
                ]
            )

            return UserRepositoryDDB.get_by_id(user_id)

        except dynamodb.exceptions.TransactionCanceledException as e:
            raise ValueError("Username or user ID already exists")

    @staticmethod
    def get_by_id(user_id):
        response = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression="PK = :pk AND SK = :sk",
            ExpressionAttributeValues={
                ":pk": {"S": f"USER#{user_id}"},
                ":sk": {"S": "PROFILE"},
            },
        )

        items = response.get("Items", [])
        if not items:
            return None

        item = items[0]
        return User(
            id=user_id,
            email=item["email"]["S"],
            username=item["username"]["S"],
            password_hash=item["password_hash"]["S"],
            name=item["name"]["S"],
            created_at=int(item["created_at"]["N"]),
        )

    @staticmethod
    def get_by_username(username):
        response = dynamodb.query(
            TableName=TABLE_NAME,
            KeyConditionExpression="PK = :pk AND SK = :sk",
            ExpressionAttributeValues={
                ":pk": {"S": f"USER#{username}"},
                ":sk": {"S": "PROFILE"},
            },
        )

        items = response.get("Items", [])
        if not items:
            return None

        item = items[0]
        return User(
            id=item["user_id"]["S"],
            email=item["email"]["S"],
            username=username,
            password_hash=item["password_hash"]["S"],
            name=item["name"]["S"],
            created_at=int(item["created_at"]["N"]),
        )

    @staticmethod
    def get_all():
        raise NotImplementedError(
            "get_all() requires Scan operation which is not allowed. "
            "Consider implementing pagination or removing this method."
        )

    @staticmethod
    def check_password(user, password):
        return bcrypt.checkpw(
            password.encode("utf-8"), user.password_hash.encode("utf-8")
        )
