class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'
class Dev(Config):
    ENV="development"
    DEBUG = True
    SECRET_KEY = 'dev'
class TestingConfig(Config):
    TESTING = True