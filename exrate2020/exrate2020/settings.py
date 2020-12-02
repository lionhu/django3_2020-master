"""
Django settings for exrate2020 project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
import datetime
from django.contrib.messages import constants as messages
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

SECRET_KEY = '2us*m@736zhmk@=3!49hm2x#%w4b2v%&n0qktr+r+(esc7hi^%'
# SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = True
# DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

# Application definition
AUTH_USER_MODEL = "authentication.User"

INSTALLED_APPS = [

    'channels',
    "testcelery",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'corsheaders',
    'imagekit',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'webpack_loader',
    "authentication",
    'rolepermissions',
    'django_celery_results',
    'django_celery_beat',
    'crispy_forms',
    'mptt',
    'django_extensions',
    'debug_toolbar',
    'treewidget',
    'qr_code',
    'user_g11n',

    # "expenses",
    # "income",
    # "userstats",
    # "upload",
    # "studydjango",
    "store",

    "chat",
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',  # This must be first on the list
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middlewares.setAccessToken.SimpleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'user_g11n.middleware.UserLanguageMiddleware',  # Add
    'user_g11n.middleware.UserTimeZoneMiddleware',  # Add
    # 'leapin.libs.multitenancy.SetCurrentTenantFromUser',
    'django.middleware.cache.FetchFromCacheMiddleware',  # This must be last
]

ROOT_URLCONF = 'exrate2020.urls'
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost'
]
# ENABLE_STACKTRACES_LOCALS=True

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',  # 模版加上 国际化i18n
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'django_settings_export.settings_export',
                "store.context_processors.store_categories",
                "store.context_processors.session_cart",
                "store.context_processors.accessToken",
            ],
        },
    },
]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
WSGI_APPLICATION = 'exrate2020.wsgi.application'
ASGI_APPLICATION = "exrate2020.routings.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],
        },
    }
}
CACHES = {
    "default": {
        # "BACKEND": "django_redis.cache.RedisCache",
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        }
    },
    'qr-code': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'qr-code-cache',
        'TIMEOUT': 3600
    }
}
QR_CODE_CACHE_ALIAS = 'qr-code'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=3),
}
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, './webpack-stats.json'),
        # 'POLL_INTERVAL': 0.1,
        # 'TIMEOUT': None,
        # 'IGNORE': ['.+\.hot-update.js', '.+\.map']
    }
}

ROLEPERMISSIONS_MODULE = 'exrate2020.roles'

BROKER_TRANSPORT_OPTIONS = {
    'visibility_timeout': 3600
}
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_TIMEZONE = 'Asia/Tokyo'
DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ('en', _('English')),
    ('zh-hans', _('中文')),
    ('ja', _('日本語')),
)

LANGUAGE_CODE = 'ja'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

# LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/webauth/login/'
LOGOUT_URL = '/webauth/logout/'

SITE_ID = 7

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '991613301101-d7a15n1idf3niaoeef689dil3hiql8gt.apps.googleusercontent.com',
            'secret': 'S9GgCHEmFAYYs7-GT8SjCAYB',
            'key': ''
        }
    }
}

EMAIL_HOST = 'nichiei09.sakura.ne.jp'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'shop@nichiei09.sakura.ne.jp'
EMAIL_HOST_PASSWORD = 'nichiei2020'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'shop@nichiei.services'

MESSAGE_TAGS = {
    messages.ERROR: "danger"
}
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# importing logger settings
try:
    from .logger_settings import LOGGING
except Exception as e:
    # in case of any error, pass silently.
    pass

CACHE_TTL = 60 * 15

# Nichiei Related
NICHIEI_INFO = {
    "SALES_EMAIL": "crs@nichiei.services",
    "SALES_PHONE": "+81 48 708 6883",
    "SALES_MAN_PHONE": "+81 70-4305-1891",
    "SALES_POSTCODE": "〒336-0031",
    "SALES_ADD": "日本埼玉県さいたま市南区鹿手袋7-19-17",

    "CONTACT_INFO_EMAIL": "huhaiguang@me.com"
}

CART_SESSION_KEY = "nichiei_cart"
CART_TEMPLATE_TAG_NAME = 'get_cart'
CART_PRODUCT_MODEL = "store.models.Item"
# CART_PRODUCT_LOOKUP = {
#     'published': True,
#     'status': 'A',
# }
VALID_USER_MARGIN_LOOKUP = {
    'is_valid': True,
}

ADMIN_NAME = "admin"
ADMIN_ID = 2
ADMIN_INTROCODE = "51fa7641-e634-44ac-a963-33675c967e5c"

SETTINGS_EXPORT = [
    'NICHIEI_INFO',
    "ADMIN_INTROCODE"
]

MARGIN_RATES = {
    "1": 0.5,
    "2": 0.3,
    "3": 0.2
}

MARGIN_CRITERIA_ORDERS = 5
