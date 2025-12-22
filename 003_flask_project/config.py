import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DATABASE = os.getenv("DATABASE", "splitwise.db")
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    HOST = "0.0.0.0"
    PORT = 5000


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
    DATABASE = ":memory:"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
