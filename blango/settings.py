from pathlib import Path
from configurations import Configuration, values
from datetime import timedelta

import os
import dj_database_url

class Dev(Configuration):

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.Argon2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
        'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    ]

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
        },
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "verbose",
            },
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
                "filters": ["require_debug_false"],
            },
        },
        "loggers": {
            "django.request": {
                "handlers": ["mail_admins"],
                "level": "ERROR",
                "propagate": True,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    }
    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-+sn%dpa!086+g+%44z9*^j^q-u4n!j(#wl)x9a%_1op@zz2+1-'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(True)

    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    ACCOUNT_ACTIVATION_DAYS = 7
    
    ALLOWED_HOSTS = ['*']
    INTERNAL_IPS = ["192.168.10.93"]
    X_FRAME_OPTIONS = 'ALLOW-FROM ' + os.environ.get('CODIO_HOSTNAME') + '-8000.codio.io'
    CSRF_COOKIE_SAMESITE = None
    CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('CODIO_HOSTNAME') + '-8000.codio.io']
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = None

    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_URL = "/media/"
    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'rest_framework.authtoken',
        'django_filters',
        'versatileimagefield',
        'crispy_forms',
        'crispy_bootstrap5',
        'debug_toolbar',
        'blango_auth',
        'blog',
    ]

    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
    CRISPY_TEMPLATE_PACK = "bootstrap5"

    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.BasicAuthentication",
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework.authentication.TokenAuthentication",
            "rest_framework_simplejwt.authentication.JWTAuthentication"
        ],
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticatedOrReadOnly"
        ],
        "DEFAULT_THROTTLE_CLASSES": [
            "blog.api.throttling.AnonSustainedThrottle",
            "blog.api.throttling.AnonBurstThrottle",
            "blog.api.throttling.UserSustainedThrottle",
            "blog.api.throttling.UserBurstThrottle",
        ],
        "DEFAULT_THROTTLE_RATES": {
            "anon_sustained": "500/day",
            "anon_burst": "10/minute",
            "user_sustained": "5000/day",
            "user_burst": "100/minute",
        },
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": 100,
        "DEFAULT_FILTER_BACKENDS": [
            "django_filters.rest_framework.DjangoFilterBackend",
            "rest_framework.filters.OrderingFilter"
        ],
    }

    SIMPLE_JWT = {
        "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    }

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        # 'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'blango.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                BASE_DIR / 'templates'
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

    WSGI_APPLICATION = 'blango.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/3.2/ref/settings/#databases

    DATABASES = {
        "default": dj_database_url.config(default=f"sqlite:///{BASE_DIR}/db.sqlite3"),
        "alternative": dj_database_url.config(
            "ALTERNATIVE_DATABASE_URL",
            default=f"sqlite:///{BASE_DIR}/alternative_db.sqlite3",
        ),
    }

    # Password validation
    # https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

    AUTH_USER_MODEL = "blango_auth.User"


    # Internationalization
    # https://docs.djangoproject.com/en/3.2/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = values.Value("UTC")

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/

    STATIC_URL = '/static/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    SWAGGER_SETTINGS = {
        "SECURITY_DEFINITIONS": {
            "Token": {"type": "apiKey", "name": "Authorization", "in": "header"},
            "Basic": {"type": "basic"},
        }
    }