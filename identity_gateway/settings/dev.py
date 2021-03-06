from .base import *

DEBUG = True

#TEST_MODE = True
#DEV_MODE = True

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = "127.0.0.1"

DEV_APPS = [
  #'debug_toolbar'
]

MIDDLEWARE_DEV = [
  #'debug_toolbar.middleware.DebugToolbarMiddleware'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'ofsted'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'OfstedB3ta'),
        'HOST': os.environ.get('POSTGRES_HOST', '130.130.52.132'),
        'PORT': os.environ.get('POSTGRES_PORT', '5462')
    }
}

MIDDLEWARE = MIDDLEWARE + MIDDLEWARE_DEV
INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + DEV_APPS + PROJECT_APPS

# SECURITY WARNING: keep the secret key used in production secre