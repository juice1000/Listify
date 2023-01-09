import os

class Config(object):
    DEBUG = False
    TESTING = False
    CELERY_TIMEZONE = os.environ.get("timezone", "Europe/Berlin")
    CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://")
    CELERY_RESULT_BACKEND = os.environ.get(
        "REDIS_URL", "redis://"
    )
    CELERY_SEND_SENT_EVENT = True
class Prod(Config):
    DOMAIN = '0.0.0.0'
class Dev(Config):
    DOMAIN = ''
    ENV="development"
    DEBUG = True
class Test(Config):
    TESTING = True
    DOMAIN = ''