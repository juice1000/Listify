class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
class Prod(Config):
    DOMAIN = '0.0.0.0'
class Dev(Config):
    DOMAIN = ''
    ENV="development"
    DEBUG = True
    SECRET_KEY = 'dev'
class Test(Config):
    TESTING = True
    DOMAIN = ''