import os

class Config(object):
    DEBUG = False
    TESTING = False
    CELERY_TIMEZONE = os.getenv("timezone", "Europe/Berlin")
    CELERY_BROKER_URL = os.getenv("broker_url", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv(
        "result_backend", "redis://localhost:6379/0"
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