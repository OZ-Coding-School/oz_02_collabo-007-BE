from .base import *
from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = False

IS_LOCAL = False

ALLOWED_HOSTS = [
    'match-point.co.kr',
    'www.match-point.co.kr',
    'admin.match-point.co.kr',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

CSRF_TRUSTED_ORIGINS = [
    'https://api.match-point.co.kr',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
}
