"""
Django settings for dms project.

Generated by 'django-admin startproject' using Django.

For more information on this file, see
https://docs.djangoproject.com/en/latest/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/latest/ref/settings/
"""

from pathlib import Path

from decouple import Csv, config
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import OperationalError

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/latest/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config("SECRET_KEY", default="Make sure to set your own secret key!")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("ENVIRONMENT", default="development") == "development"

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    cast=Csv(),
    default="localhost,127.0.0.1,dev.tawalabora.space",
)

# Application definition

CUSTOM_APP_NAME = config("CUSTOM_APP_NAME", default=None)
CUSTOM_APP_URL = config("CUSTOM_APP_URL", default="dashboard/")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sass_processor",
    "phonenumber_field",
    "apps.core",
    "apps.home",
    "apps.seed",
]

# Add Custom app
if CUSTOM_APP_NAME:
    INSTALLED_APPS.append(CUSTOM_APP_NAME)

# Add django_browser_reload only in DEBUG mode
if DEBUG:
    INSTALLED_APPS.append("django_browser_reload")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Add django_browser_reload middleware only in DEBUG mode
if DEBUG:
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")


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

ROOT_URLCONF = "conf.urls"
WSGI_APPLICATION = "conf.wsgi.application"


# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
# https://docs.djangoproject.com/en/stable/ref/databases/

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "lib" / config("DB_NAME", default="db.sqlite3"),
    }
}

# Only use PostgreSQL if explicitly configured
if config("DB_POSTGRESQL", default=False, cast=bool):
    try:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": config("DB_NAME", default=None),
                "USER": config("DB_USER", default=None),
                "PASSWORD": config("DB_PASSWORD", default=None),
                "HOST": config("DB_HOST", default="localhost"),
                "PORT": config("DB_PORT", default="5432"),
            }
        }
    except (ImproperlyConfigured, OperationalError, ModuleNotFoundError):
        pass  # Falls back to SQLite


# Authentication & Password Validation
# https://docs.djangoproject.com/en/latest/ref/settings/#auth
# https://docs.djangoproject.com/en/latest/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "core.User"

AUTHENTICATION_BACKENDS = [
    # * Ensure your custom backend is the first in this list
    # "app.core.authentication.backends.PhoneAuthBackend",
    "django.contrib.auth.backends.ModelBackend",  # Keep the default auth backend
]

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


# Internationalization
# https://docs.djangoproject.com/en/latest/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/latest/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

STATIC_URL = "lib/static/"
STATIC_ROOT = BASE_DIR / "lib" / "static"

SASS_PRECISION = 8


# Media files
# https://docs.djangoproject.com/en/latest/ref/settings/#media-files

MEDIA_URL = "lib/media/"
MEDIA_ROOT = BASE_DIR / "lib" / "media"


# Default primary key field type
# https://docs.djangoproject.com/en/latest/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Email
# https://docs.djangoproject.com/en/latest/topics/email/

EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = "587"
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default=None)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default=None)
EMAIL_HOST = config("EMAIL_HOST", default=None)


# Cache
# https://docs.djangoproject.com/en/stable/topics/cache/

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": config("CACHE_LOCATION", default="django_cache"),
        "TIMEOUT": 300,  # Optional: Default cache timeout in seconds (e.g., 5 minutes)
        "OPTIONS": {
            "MAX_ENTRIES": 1000  # Optional: Max number of entries in the cache table
        },
    }
}

