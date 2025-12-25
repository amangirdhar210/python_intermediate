# Splitwise Clone

A Flask-based expense splitting application with DynamoDB backend, clean architecture and minimal dependencies.

## Features

- User authentication (register/login)
- Create and manage groups
- Add expenses and split equally among group members
- Automatic balance calculation with debt simplification
- Settle up functionality
- Clean, responsive UI

## Project Structure

```
003_flask_project/
├── app/
│   ├── __init__.py
│   ├── dynamo_schema.json
│   ├── models/
│   │   └── user.py
│   ├── ddb_repo/
│   │   ├── user_ddb_repo.py
│   │   ├── group_ddb_repo.py
│   │   ├── expense_ddb_repo.py
│   │   └── settlement_ddb_repo.py
│   ├── repositories/
│   │   └── __init__.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── group_service.py
│   │   ├── expense_service.py
│   │   └── balance_service.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── groups.py
│   │   ├── expenses.py
│   │   ├── settlements.py
│   │   └── main.py
│   ├── templates/
│   └── static/
├── config.py
├── run.py
└── requirements.txt
```

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables:

```bash
export AWS_REGION=us-east-1
export DYNAMODB_TABLE_NAME=ExpenseSplitApp
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export SECRET_KEY=your_flask_secret_key
```

3. Create DynamoDB table using the schema in `app/dynamo_schema.json`:

```bash
aws dynamodb create-table \
    --table-name ExpenseSplitApp \
    --attribute-definitions \
        AttributeName=PK,AttributeType=S \
        AttributeName=SK,AttributeType=S \
    --key-schema \
        AttributeName=PK,KeyType=HASH \
        AttributeName=SK,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST
```

4. Run the application:

```bash
python run.py
```

5. Access at http://localhost:5000

## Architecture

- **Models**: User model for Flask-Login integration
- **DDB Repositories**: Data access layer with DynamoDB operations
- **Services**: Business logic layer for expense splitting and balance calculation
- **Routes**: Flask blueprints for handling HTTP requests
- **Templates**: Jinja2 templates for UI rendering

## Database

DynamoDB single-table design with the following access patterns:

- User Profile by ID: `PK=USER#<user_id>`, `SK=PROFILE`
- User Profile by Username: `PK=USER#<username>`, `SK=PROFILE`
- User's Groups: `PK=USER#<user_id>`, `SK=GROUP#<group_id>`
- Group Metadata: `PK=GROUP#<group_id>`, `SK=Group_Info`
- Group Expenses: `PK=GROUP#<group_id>`, `SK=EXPENSE#<created_at>#<expense_id>`
- Group Settlements: `PK=GROUP#<group_id>`, `SK=SETTLEMENT#<created_at>#<settlement_id>`

See `app/dynamo_schema.json` for complete schema details.
