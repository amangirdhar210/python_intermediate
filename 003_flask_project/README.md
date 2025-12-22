# Splitwise Clone

A Flask-based expense splitting application with clean architecture and minimal dependencies.

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
│   ├── models/
│   │   ├── user.py
│   │   ├── group.py
│   │   ├── expense.py
│   │   ├── settlement.py
│   │   ├── group_member.py
│   │   └── expense_split.py
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── group_repository.py
│   │   ├── expense_repository.py
│   │   └── settlement_repository.py
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
cp .env.example .env
```

3. Run the application:

```bash
python run.py
```

4. Access at http://localhost:5000

## Architecture

- **Models**: SQLAlchemy ORM models for database schema
- **Repositories**: Data access layer with database operations
- **Services**: Business logic layer for expense splitting and balance calculation
- **Routes**: Flask blueprints for handling HTTP requests
- **Templates**: Jinja2 templates for UI rendering

## Database

SQLite database with the following tables:

- users
- groups
- group_members
- expenses
- expense_splits
- settlements
