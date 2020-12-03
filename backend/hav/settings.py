"""
Django settings for hav project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import sys
import logging.config
from django.utils.log import DEFAULT_LOGGING
import environ
from pathlib import Path
from dj_database_url import parse as parse_db_url

from .image_resolutions import resolutions as IMAGE_RESOLUTIONS

# this is needed to let daphne install the twisted reactor
import daphne.server  # noqa

# register custom mimetypes
import hav_utils.mimetypes  # noqa

project_root = environ.Path(__file__) - 3
django_root = environ.Path(__file__) - 2


# set up the environment
env = environ.Env(
    DEBUG=(bool, False),
    DJANGO_SECRET_KEY=str,
    DRF_AUTH_TOKEN=(str, ""),
    ALLOWED_HOSTS=(list, ["*"]),
    SENTRY_DSN=(str, ""),
    LOGLEVEL=(str, "debug"),
    IMAGINARY_SECRET=str,
    IMAGINARY_URL_PREFIX=(str, "/images/"),
    WEBASSET_URL_PREFIX=(str, "http://127.0.0.1:9000"),
    WEBASSET_BASE_URL=(str, "/webassets/"),
    CACHE_URL=(str, "redis://127.0.0.1:6379/0"),
    DATABASE_URL=(str, "postgres:///hav"),
    WHAV_DATABASE_URL=(str, "postgres:///whav"),
    HAV_SKOSMOS_URL=(str, "https://skosmos-hav.aussereurop.univie.ac.at/rest/v1/"),
)

# read the .env file
environ.Env.read_env(project_root(".env"))

DEBUG = env("DEBUG", False)

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

DRF_AUTH_TOKEN = env("DRF_AUTH_TOKEN")

INSTALLED_APPS = [
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "webpack_loader",
    "rest_framework",
    "rest_framework.authtoken",
    "treebeard",
    "channels_redis",
    "corsheaders",
    "django_rq",
    "graphene_django",
    "apps.whav",
    "apps.sets",
    "apps.archive",
    "apps.media",
    "apps.ingest",
    "apps.webassets",
    "apps.hav_collections",
    "apps.tags",
    "sources.uploads",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + ["debug_toolbar", "django_extensions"]

    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

    INTERNAL_IPS = ["127.0.0.1"]


ROOT_URLCONF = "hav.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [django_root("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "hav.wsgi.application"


DATABASES = {
    "default": parse_db_url(env("DATABASE_URL")),
    "whav": parse_db_url(env("WHAV_DATABASE_URL")),
}


DATABASE_ROUTERS = ["hav.db_router.WhavDBRouter"]

CACHES = {"default": env.cache()}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    )
}

WEBPACK_BUILD_PATH = project_root("frontend/admin/build/")


WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "/",
        "STATS_FILE": Path(WEBPACK_BUILD_PATH) / "webpack-stats.json",
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        "IGNORE": [".+\.hot-update.js", ".+\.map"],
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = "/static/"

STATICFILES_DIRS = (("wp", WEBPACK_BUILD_PATH), ("dj_static", django_root("static/")))

STATIC_ROOT = project_root(env("STATIC_ROOT", default="dist/static/"))

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

MEDIA_URL = "/media/"

MEDIA_ROOT = project_root(env("DJANGO_MEDIA_ROOT", default="dist/media/"))

STORAGES = {
    "webassets": {
        "location": project_root(env("WEBASSET_ROOT", default="dist/webassets/")),
        "base_url": env("WEBASSET_BASE_URL"),
        "storage_class": "hav_utils.storages.ProtectedFileSystemStorage",
    }
}

print(STORAGES)

LOGIN_URL = "admin:login"


ASGI_APPLICATION = "hav.asgi.application"

cache_config = env.cache("CACHE_URL")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [f'{cache_config["LOCATION"]}']},
    }
}


# Disable Django's logging setup
LOGGING_CONFIG = None

LOGLEVEL = env("LOGLEVEL").upper()


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                # exact format is not important, this is the minimum information
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
            },
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "handlers": {
            # console logs to stderr
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": sys.stdout,
            },
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            # default for all undefined Python modules
            "": {"level": "WARNING", "handlers": ["console"]},
            # Our application code
            "apps": {
                "level": LOGLEVEL,
                "handlers": ["console"],
                # Avoid double logging because of root logger
                "propagate": False,
            },
            # Prevent noisy modules from logging
            # 'noisy_module': {
            #     'level': 'ERROR',
            #     'handlers': ['console'],
            #     'propagate': False,
            # },
            # Default runserver request logging
            "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
            "django.channels.server": DEFAULT_LOGGING["loggers"]["django.server"],
        },
    }
)

IMAGESERVER_CONFIG = {
    "prefix": env("IMAGINARY_URL_PREFIX"),
    "secret": env("IMAGINARY_SECRET"),
}

# These settings will change ....
INCOMING_FILES_ROOT = project_root(env("INCOMING_FILES_ROOT", default="dist/incoming"))
HAV_ARCHIVE_PATH = project_root(env("HAV_ARCHIVE_PATH", default="dist/archive"))

WHAV_ARCHIVE_PATH = project_root(env("WHAV_ARCHIVE_PATH", default="dist/whav"))

# this is not nice
INGEST_LOG_DIR = project_root(env("INGEST_LOG_DIR", default="dist/ingestlog"))

INGESTION_SOURCES = {
    "whav": {"engine": "sources.whav.WHAVSource", "db": "whav"},
    "incoming": {"engine": "sources.filesystem.FSSource", "root": INCOMING_FILES_ROOT},
    "uploads": {
        "engine": "source.uploads.UploadSource",
        "root": project_root(env("UPLOADS_ROOT", default=MEDIA_ROOT)),
    },
}

RQ_QUEUES = {
    "default": {"USE_REDIS_CACHE": "default"},
    "webassets": {"USE_REDIS_CACHE": "default"},
    "archive": {"USE_REDIS_CACHE": "default"},
}

GRAPHENE = {"SCHEMA": "api.graphql.schema"}

if env("SENTRY_DSN"):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.rq import RqIntegration

    sentry_sdk.init(
        env("SENTRY_DSN"), integrations=[DjangoIntegration(), RqIntegration()]
    )

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# allow all CORS in debug mode
# CORS_ORIGIN_ALLOW_ALL = DEBUG

CORS_ORIGIN_WHITELIST = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8001",
    "http://127.0.0.1:8001",
    "https://hav-preview.netlify.com",
]

# CORS_ORIGIN_REGEX_WHITELIST = [
#     r"^https://\w+\.netlify\.com$",
# ]

# TAGGING
TAGGING_SOURCES = {
    "skosmos": {
        "source": "apps.tags.sources.skosmos.Source",
        "options": {"url": env("HAV_SKOSMOS_URL")},
    },
    "languages": {"source": "apps.tags.sources.iso639_3.Source"},
    "countries": {"source": "apps.tags.sources.iso3166.Source"},
}

# TEST Setup
if "test" in sys.argv:
    for key in RQ_QUEUES:
        RQ_QUEUES[key].update({"ASYNC": False, "DB": 5})

    FIXTURE_DIRS = (django_root("fixtures"),)
