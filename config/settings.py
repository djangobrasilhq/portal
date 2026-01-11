"""
Django settings for config project.
"""

import logging
from pathlib import Path

import os
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = os.getenv("SECRET_KEY")

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "social_django",
    "accounts",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "social_core.backends.github.GithubOAuth2",
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_USER_MODEL = "accounts.User"

# Configurações do GitHub OAuth
SOCIAL_AUTH_GITHUB_KEY = os.getenv("GITHUB_CLIENT_ID")
SOCIAL_AUTH_GITHUB_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

# URL de redirecionamento após login
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/"
SOCIAL_AUTH_LOGIN_ERROR_URL = "/"

# Configurações de sessão para OAuth
# IMPORTANTE: Use sempre o mesmo host (localhost OU 127.0.0.1) durante todo o processo
if os.getenv("LOCAL", False) or DEBUG:
    # Aumenta o tempo de expiração do state em desenvolvimento
    SOCIAL_AUTH_STATE_TIMEOUT = 600  # 10 minutos
    # Garante que o state seja armazenado corretamente na sessão
    SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ["state"]

# Em desenvolvimento local, configurações para garantir redirect_uri correto
if os.getenv("LOCAL", False) or DEBUG:
    # Garante que o Django use localhost para construir URLs absolutas em desenvolvimento
    USE_X_FORWARDED_HOST = False
    USE_X_FORWARDED_PORT = False
    # Força o uso de HTTP (não HTTPS) em desenvolvimento
    SOCIAL_AUTH_REDIRECT_IS_HTTPS = False

# Pipeline de autenticação (cria usuário automaticamente se não existir)
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [BASE_DIR / "static"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = "static/"

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

EMAIL_BACKEND = os.getenv(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)

# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Filipe Martins""", "filipe@fmartns.dev")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

if os.getenv("LOCAL", False):
    # https://docs.djangoproject.com/en/dev/ref/settings/#caches
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "",
        }
    }

    # https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = os.getenv(
        "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
    )

    # http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
    INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405

    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
    INSTALLED_APPS += ["debug_toolbar"]  # noqa F405

    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405

    # https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": [
            "debug_toolbar.panels.redirects.RedirectsPanel",
            "debug_toolbar.panels.profiling.ProfilingPanel",
        ],
        "SHOW_TEMPLATE_CONTEXT": True,
    }

    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
    if os.getenv("USE_DOCKER", False):
        import socket

        hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
        INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]
        try:
            _, _, ips = socket.gethostbyname_ex("node")
            INTERNAL_IPS.extend(ips)
        except socket.gaierror:
            # The node container isn't started (yet?)
            pass

    # https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
    INSTALLED_APPS += ["django_extensions"]  # noqa F405

else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.getenv("REDIS_URL"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
                "IGNORE_EXCEPTIONS": True,
            },
        }
    }

    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", True)

    # https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
    SESSION_COOKIE_SECURE = True

    # https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
    CSRF_COOKIE_SECURE = True

    # https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
    # TODO: set this to 60 seconds first and then to 518400 once you prove the former works
    SECURE_HSTS_SECONDS = 60

    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv(
        "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
    )

    # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
    SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", True)

    # https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
    SECURE_CONTENT_TYPE_NOSNIFF = os.getenv("SECURE_CONTENT_TYPE_NOSNIFF", True)

    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    # https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
    DEFAULT_FROM_EMAIL = os.getenv(
        "DEFAULT_FROM_EMAIL",
        default="DjangoCon 2025 <noreply@2025.djangocon.eu>",
    )

    # https://docs.djangoproject.com/en/dev/ref/settings/#server-email
    SERVER_EMAIL = os.getenv("SERVER_EMAIL", DEFAULT_FROM_EMAIL)

    # https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
    EMAIL_SUBJECT_PREFIX = os.getenv(
        "EMAIL_SUBJECT_PREFIX",
        default="[Django Brasil]",
    )

    # ADMIN
    # ------------------------------------------------------------------------------
    # Django Admin URL regex.
    ADMIN_URL = os.getenv("ADMIN_URL", "admin/")

    # Anymail
    # ------------------------------------------------------------------------------
    # https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
    INSTALLED_APPS += ["anymail"]  # noqa F405

    # https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    # https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
    # https://anymail.readthedocs.io/en/stable/esps/mailgun/
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    ANYMAIL = {
        "MAILGUN_API_KEY": os.getenv("MAILGUN_API_KEY"),
        "MAILGUN_SENDER_DOMAIN": os.getenv("MAILGUN_DOMAIN"),
        "MAILGUN_API_URL": os.getenv("MAILGUN_API_URL", "https://api.mailgun.net/v3"),
    }

    # https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # See https://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
        "loggers": {
            "django.db.backends": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": False,
            },
            # Errors logged by the SDK itself
            "sentry_sdk": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": False,
            },
            "django.security.DisallowedHost": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }

    # Sentry
    # ------------------------------------------------------------------------------
    SENTRY_DSN = os.getenv("SENTRY_DSN")
    SENTRY_LOG_LEVEL = os.getenv("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

    sentry_logging = LoggingIntegration(
        level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors as events
    )
    integrations = [
        sentry_logging,
        DjangoIntegration(),
        RedisIntegration(),
    ]
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=integrations,
        environment=os.getenv("SENTRY_ENVIRONMENT", "production"),
        traces_sample_rate=os.getenv("SENTRY_TRACES_SAMPLE_RATE", 0.0),
    )
