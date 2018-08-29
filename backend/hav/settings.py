"""
Django settings for hav project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import environ
import logging.config
from django.utils.log import DEFAULT_LOGGING

from .image_resolutions import resolutions as IMAGE_RESOLUTIONS

# this is needed to let daphne install the twisted reactor
import daphne.server # noqa


project_root = environ.Path(__file__) - 3
django_root = environ.Path(__file__) - 2


# set up the environment
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "VERY_VERY_UNSAFE"),
    ALLOWED_HOSTS=(list, []),
    SENTRY_DSN=(str, ''),
    LOGLEVEL=(str, 'info'),
    URL_SIGNATURE_KEY=(str, 'quite_unsafe_i_must_say'),
    IMAGESERVER_URL_PREFIX=(str, '/'),
    WEBASSET_URL_PREFIX=(str, 'http://127.0.0.1:9000')
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
    'django_celery_results',
    'treebeard',
    'channels',
    'apps.whav',
    'apps.sets',
    'apps.archive',
    'apps.media',
    'apps.ingest',
    'apps.webassets',
    'apps.hav_collections',
    'raven.contrib.django.raven_compat',
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


if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + [
        'debug_toolbar'
    ]

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    ] + MIDDLEWARE

    INTERNAL_IPS = [
        '127.0.0.1'
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
    'default': env.db('DATABASE_URL', 'postgres:///hav'),
    'whav': env.db('WHAV_DATABASE_URL', 'postgres:///whav')
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
    ('dj_static', django_root('static/'))
)

STATIC_ROOT = project_root(env('STATIC_ROOT', default='dist/static/'))

MEDIA_URL = '/media/'

MEDIA_ROOT = project_root(env('MEDIA_ROOT', default='dist/media/'))

STORAGES = {
    'webassets': {
        'location': project_root(
            env(
                'WEBASSET_ROOT',
                default='dist/webassets/'
            )
        ),
        'base_url': env('WEBASSET_URL_PREFIX'),
        'storage_class': 'hav.utils.storages.ProtectedFileSystemStorage'
    }
}

LOGIN_URL = 'admin:login'

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/1')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='django-db')

# 10 days expiration for results
CELERY_RESULT_EXPIRES = 3600 * 24 * 10

# use json format for everything
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TASK_ROUTES = {
    'apps.webassets.tasks.*': {
        'queue': 'webassets'
    },
    'apps.archive.tasks.*': {
        'queue': 'archive'
    }
}

# CELERY_WORKER_HIJACK_ROOT_LOGGER = False

ASGI_APPLICATION = "hav.routing.application"

RAVEN_CONFIG = {
    'dsn': env('SENTRY_DSN'),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(project_root()),
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
            'handlers': [
                'console', 'sentry'],
        },
        # Our application code
        'app': {
            'level': LOGLEVEL,
            'handlers': [
                'console',
                'sentry'
            ],
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

IMAGESERVER_CONFIG = {
    'prefix': env('IMAGESERVER_URL_PREFIX'),
    'secret': env('URL_SIGNATURE_KEY')
}

# These settings will change ....
INCOMING_FILES_ROOT = project_root(env('INCOMING_FILES_ROOT', default='dist/incoming'))
HAV_ARCHIVE_PATH = project_root(env('HAV_ARCHIVE_PATH', default='dist/archive'))

WHAV_ARCHIVE_PATH = project_root(
    env(
        'WHAV_ARCHIVE_PATH',
        default='dist/whav'
    )
)

INGESTION_SOURCES = {
    "whav": {
        "engine": "sources.whav.WHAVSource",
        "db": "whav",

    },
    "incoming": {
        "engine": "sources.filesystem.FSSource",
        "root": INCOMING_FILES_ROOT
    }
}
