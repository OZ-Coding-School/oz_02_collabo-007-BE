from .base import *

DEBUG = True

# 로컬 환경에서는 True로 설정하고, 서버 환경에서는 False로 설정합니다.
IS_LOCAL = True

ALLOWED_HOSTS = []  # postman 테스트를 위해 *로 잠시 세팅

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
