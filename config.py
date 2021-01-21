import os

#-------------Day 3 AWS S3 -----------------------------

S3_BUCKET   = os.environ.get("S3_BUCKET_NAME")
S3_KEY      = os.environ.get("S3_ACCESS_KEY")
S3_SECRET   = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

#-----------------End-----------------------------------
#-------------Day 5 OAuth -----------------------------

#-----------------End-----------------------------------


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    G_CLIENT_ID = os.environ.get("G_CLIENT_ID")
    G_CLIENT_SECRET = os.environ.get("G_CLIENT_SECRET")


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
