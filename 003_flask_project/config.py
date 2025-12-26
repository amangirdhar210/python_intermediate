import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    HOST = "0.0.0.0"
    PORT = 5000
    DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "ExpenseSplitApp")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
