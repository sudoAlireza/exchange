import logging
from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = []

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "drf_spectacular",
]

LOCAL_APPS = [
    "currency",
    "order",
    "user",
    "wallet",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

SPECTACULAR_SETTINGS = {
    "TITLE": "Exchange API",
    "DESCRIPTION": "Simple exchange api documentation",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAuthenticated"],
}
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "request_logging.middleware.LoggingMiddleware",
]

REQUEST_LOGGING_DATA_LOG_LEVEL = logging.INFO  # django-request-logging
REQUEST_LOGGING_ENABLE_COLORIZE = False
DJANGO_REQUEST_LOGGING_LOG_HEADERS_DEFAULT_VALUE = True
DJANGO_REQUEST_LOGGING_LOG_RESPONSE_DEFAULT_VALUE = True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "ignore_openapi_logs": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: not record.getMessage().startswith("b'"),
        },
    },
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "timestamp": True,
            "json_ensure_ascii": False,
            "reserved_attrs": (
                "args",
                "asctime",
                "created",
                "exc_info",
                "exc_text",
                "filename",
                "funcName",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "msg",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "stack_info",
                "thread",
                "threadName",
            ),
        },
    },
    "handlers": {
        "console": {
            "level": logging.getLevelName(os.environ.get("APP_LOG_LEVEL", "INFO").upper()),
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": logging.getLevelName(os.environ.get("APP_LOG_LEVEL", "INFO").upper()),
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console"],
            "level": logging.getLevelName(os.environ.get("APP_LOG_LEVEL", "INFO").upper()),
            "filters": ["ignore_openapi_logs"],
            "propagate": False,
        },
    },
    "root": {
        "level": logging.getLevelName(os.environ.get("APP_LOG_LEVEL", "INFO").upper()),
        "handlers": ["console"],
    },
}


ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("DATABASE_PORT", "5432"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

AUTH_USER_MODEL = "user.User"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


BINANCE_BUY_CURRENCY_API = os.environ.get("BINANCE_BUY_CURRENCY_API")
BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")