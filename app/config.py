# app/config.py
import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False