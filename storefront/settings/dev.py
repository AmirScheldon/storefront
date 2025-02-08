from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-q-nnul*ke2c@mq4i#y)rv@o6wab)&)rz^ik()!+08urw3dj0=v'

CELERY_BROKER_URL = 'redis://redis:6379/1'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/2",
        'TIMEOUT': 10 * 60, #second
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_HOST = 'smtp4dev'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOBAR_CALLBACK': lambda request: True
}