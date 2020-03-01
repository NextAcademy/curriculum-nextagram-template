import os

SECRET_KEY = os.urandom(32)
DEBUG = True
PORT = 5000


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    S3_BUCKET = os.environ.get("S3_BUCKET")
    S3_KEY = os.environ.get("ACCESS_KEY")
    S3_SECRET = os.environ.get("SECRET_ACCESS_KEY")
    S3_LOCATION = f'http://{S3_BUCKET}.s3.amazonaws.com/'


class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
