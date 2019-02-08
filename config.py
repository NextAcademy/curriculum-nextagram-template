import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or b'{;m\x18\xc5W{-zv\x9b@\xa0{|j\\\xa5\x0f\x19\x9b\x874\x88\xf8\xf2\xf1\xfc\x8cOm\xeb'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
