"""
Django settings for hav project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import environ
import raven
import logging.config
from django.utils.log import DEFAULT_LOGGING

project_root = environ.Path(__file__) - 3
django_root = environ.Path(__file__) - 2

# set up the environment
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    SENTRY_DSN=(str, ''),
    LOGLEVEL=(str, 'info')
)

# read the .env file
environ.Env.read_env(project_root('.env'))


DEBUG = env('DEBUG', False)

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'webpack_loader',
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_monitor',
    'django_celery_results',
    'treebeard',
    'raven.contrib.django.raven_compat',
    'apps.whav',
    'apps.sets',
    'apps.archive',
    'apps.media',
    'apps.ingest'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hav.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            django_root('templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hav.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env('HAV_DB_HOST', default=''),
        'PORT': env('HAV_DB_PORT', default=''),
        'NAME': env('HAV_DB_NAME', default='hav'),
        'USER': env('HAV_DB_USER', default=''),
        'PASSWORD': env('HAV_DB_PW', default=''),
        'ATOMIC_REQUESTS': True

    },
    'whav': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env('WHAV_DB_HOST', default=''),
        'PORT': env('WHAV_DB_PORT', default=''),
        'NAME': env('WHAV_DB_NAME', default='whav'),
        'USER': env('WHAV_DB_USER', default=''),
        'PASSWORD': env('HAV_DB_PW', default=''),
        'ATOMIC_REQUESTS': True
    },
}


DATABASE_ROUTERS = [
    'hav.db_router.WhavDBRouter'
]

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

WEBPACK_BUILD_PATH = project_root('frontend/build/')

WEBPACK_ASSET_PATH = project_root('frontend/src/assets/')

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': '/',
        'STATS_FILE': project_root('frontend/build/webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': ['.+\.hot-update.js', '.+\.map']
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    ('wp', WEBPACK_BUILD_PATH),
    ('frontend_assets', WEBPACK_ASSET_PATH)
)

MEDIA_URL = '/media/'

MEDIA_ROOT = env('MEDIA_ROOT', default=project_root('dist/media/'))

STORAGES = {
    'examples': {
        'path': project_root('dist/examples/')
    }
}

LOGIN_URL = 'admin:login'

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/1')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default=CELERY_BROKER_URL)

# 10 days expiration for results
CELERY_RESULT_EXPIRES = 3600 * 24 * 10

# use json format for everything
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

RAVEN_CONFIG = {
    'dsn': env('SENTRY_DSN'),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(project_root()),
}


# Disable Django's logging setup
LOGGING_CONFIG = None

LOGLEVEL = env('LOGLEVEL').upper()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        # console logs to stderr
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        # Add Handler for Sentry for `warning` and above
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        # default for all undefined Python modules
        '': {
            'level': 'WARNING',
            'handlers': ['console', 'sentry'],
        },
        # Our application code
        'app': {
            'level': LOGLEVEL,
            'handlers': ['console', 'sentry'],
            # Avoid double logging because of root logger
            'propagate': False,
        },
        # Prevent noisy modules from logging to Sentry
        # 'noisy_module': {
        #     'level': 'ERROR',
        #     'handlers': ['console'],
        #     'propagate': False,
        # },
        # Default runserver request logging
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
})


THUMBOR_SERVER = env('THUMBOR_SERVER', default='')
THUMBOR_SECRET_KEY = env('THUMBOR_SECRET_KEY', default='')

# These settings will change ....
INCOMING_FILES_ROOT = env('INCOMING_FILES_ROOT', default=MEDIA_ROOT)

HAV_ARCHIVE_PATH = env('HAV_ARCHIVE_PATH', default=project_root('dist/archive'))



INGESTION_SOURCES = {
    "whav": {
        "engine": "sources.whav.WHAVSource",
        "db": "whav"
    },
    "incoming": {
        "engine": "sources.filesystem.FSSource",
        "root": INCOMING_FILES_ROOT
    }
}


