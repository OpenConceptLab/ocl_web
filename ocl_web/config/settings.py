# -*- coding: utf-8 -*-
"""
Django settings for ocl_web project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join

# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
try:
    from S3 import CallingFormat
    AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN
except ImportError:
    # TODO: Fix this where even if in Dev this class is called.
    pass

from configurations import Configuration, values

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Common(Configuration):
    """ manage.py Command 'settings' to setup environment """

    BASE_URL = values.Value(default='http://localhost:7000',environ_name='BASE_URL', environ_prefix=None)

    DEFAULT_FROM_EMAIL = 'noreply@openconceptlab.org'
    ACCOUNT_EMAIL_SUBJECT_PREFIX = '[openconceptlab.org] '

    USE_X_FORWARDED_HOST = True

    ########## APP CONFIGURATION
    DJANGO_APPS = (
        # Default Django apps:
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # Useful template tags:
        # 'django.contrib.humanize',

        # Admin
        'django.contrib.admin',
    )
    THIRD_PARTY_APPS = (
        'south',  #  Database migration helpers:
        'crispy_forms',  #  Form layouts
        'avatar',  #  For user avatars
        'bootstrap3',
    )

    # Apps specific for this project go here.
    LOCAL_APPS = (
        'users',  # custom users app
        'apps.core',
        # Your stuff: custom apps go here
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    INSTALLED_APPS += (
        # Needs to come last for now because of a weird edge case between
        #   South and allauth
        'allauth',  # registration
        'allauth.account',  # registration
        'allauth.socialaccount',  # registration
        'django.contrib.humanize', # user-friendly django template tags
    )
    ########## END APP CONFIGURATION

    ########## SITE CONFIGURATION
    # Hosts/domain names that are valid for this site
    # See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '.openconceptlab.org', '.openmrs.org']
    ########## END SITE CONFIGURATION

    ########## MIDDLEWARE CONFIGURATION
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )
    ########## END MIDDLEWARE CONFIGURATION

    ########## DEBUG
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = values.BooleanValue(False)

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
    TEMPLATE_DEBUG = DEBUG
    ########## END DEBUG

    ########## FIXTURE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
    FIXTURE_DIRS = (
        join(BASE_DIR, 'fixtures'),
    )
    ########## END FIXTURE CONFIGURATION

    ########## EMAIL CONFIGURATION
    EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')
    DEFAULT_FROM_EMAIL = values.Value('openconceptlab <noreply@openconceptlab.org>')
    EMAIL_HOST = values.Value(environ_name="EMAIL_HOST", environ_prefix="")
    EMAIL_HOST_PASSWORD = values.Value(environ_name="EMAIL_HOST_PASSWORD", environ_prefix="", default="")
    EMAIL_HOST_USER = values.Value(environ_name="EMAIL_HOST_USER", environ_prefix="")
    EMAIL_PORT = values.IntegerValue(environ_name="EMAIL_PORT", environ_prefix="", default=587)
    EMAIL_USE_TLS = values.BooleanValue(environ_name="EMAIL_USE_TLS", environ_prefix="", default=True)
    EMAIL_USE_SSL = values.BooleanValue(environ_name="EMAIL_USE_SSL", environ_prefix="", default=False)
    EMAIL_SUBJECT_PREFIX = values.Value('[openconceptlab.org] ')
    ########## END EMAIL CONFIGURATION

    ########## MANAGER CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
    ADMINS = (
        ('Jonathan Payne', 'paynejd@gmail.com')
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
    MANAGERS = ADMINS
    ########## END MANAGER CONFIGURATION

    ########## DATABASE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
    DATABASES = values.DatabaseURLValue('postgres://ocl:Ocl123@dbweb.openconceptlab.org:5432/ocl')
    ########## END DATABASE CONFIGURATION

    ########## CACHING
    # Do this here because thanks to django-pylibmc-sasl and pylibmc memcacheify is
    # painful to install on windows. memcacheify is what's used in Production
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': ''
        }
    }
    ########## END CACHING

    ########## GENERAL CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
    TIME_ZONE = 'America/New_York'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
    LANGUAGE_CODE = 'en-us'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
    SITE_ID = 1

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
    USE_I18N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
    USE_L10N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
    USE_TZ = True
    ########## END GENERAL CONFIGURATION

    ########## TEMPLATE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        "allauth.account.context_processors.account",
        "allauth.socialaccount.context_processors.socialaccount",
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
        # Your stuff: custom template context processers go here
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
    TEMPLATE_DIRS = (
        join(BASE_DIR, 'templates'),
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    # See: http://django-crispy-forms.readthedocs.org/en/latest/install.html#template-packs
    CRISPY_TEMPLATE_PACK = 'bootstrap3'
    ########## END TEMPLATE CONFIGURATION

    ########## STATIC FILE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    STATIC_ROOT = join(os.path.dirname(BASE_DIR), 'staticfiles')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = '/static/'

    # See:
    # https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
    STATICFILES_DIRS = (
        join(BASE_DIR, 'static'),
    )

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
    ########## END STATIC FILE CONFIGURATION

    ########## MEDIA CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = join(BASE_DIR, 'media')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = '/media/'
    ########## END MEDIA CONFIGURATION

    ########## URL Configuration
    ROOT_URLCONF = 'config.urls'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
    WSGI_APPLICATION = 'config.wsgi.application'
    ########## End URL Configuration

    ########## AUTHENTICATION CONFIGURATION
    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",
        "allauth.account.auth_backends.AuthenticationBackend",
    )

    # Some really nice defaults
    ACCOUNT_AUTHENTICATION_METHOD = "username"
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
    ACCOUNT_SIGNUP_FORM_CLASS = 'users.forms.SignupForm'
    ACCOUNT_ADAPTER = 'users.adapter.OCLAccountAdapter'

    ########## END AUTHENTICATION CONFIGURATION

    ########## Custom user app defaults
    # Select the correct user model
    AUTH_USER_MODEL = "users.User"
    LOGIN_REDIRECT_URL = "users:redirect"
    ########## END Custom user app defaults

    ########## SLUGLIFIER
    AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"
    ########## END SLUGLIFIER

    ########## LOGGING CONFIGURATION
    def ignore_404_and_401_errors(record):
        if ' 404' in record.message or ' 401' in record.message:
            return False
        return True

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
            'ignore_404_errors': {
                '()': 'django.utils.log.CallbackFilter',
                'callback': ignore_404_and_401_errors
            }
        },

        'formatters': {
            'normal': {
                'format': "%(levelname)s %(asctime)s [%(module)s %(filename)s:%(lineno)s %(funcName)s()] %(message)s",
                'datefmt': "%Y/%m/%d %H:%M:%S"
            },
        },

        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'filters': ['ignore_404_errors', 'require_debug_false'],
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                'tags': {'custom-tag': 'x'},
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'normal',
            },
            'logfile': {
                'level': 'DEBUG',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'when': 'midnight',
                'filename': os.path.join(BASE_DIR, 'oclweb.log'),
                'formatter': 'normal',
            },
        },

        'loggers': {
            'django.request': {
                'handlers': ['mail_admins', 'console', 'logfile', 'sentry'],
                'level': 'DEBUG',
            },
            'oclapi.request': {
                'handlers': ['console', 'logfile', 'sentry'],
                'level': 'INFO',
            },
            'oclapi': {
                'handlers': ['console', 'logfile', 'sentry'],
                'level': 'DEBUG',
            },
            '': {
                'handlers': ['console', 'logfile', 'sentry'],
                'level': 'INFO',
            },
        }
    }
    ########## END LOGGING CONFIGURATION


    ########## Your common stuff: Below this line define 3rd party libary settings
    # API_HOST = 'http://65.99.230.144'
    # API_TOKEN = 'Token ' + '%s' % os.environ.get('OCL_API_TOKEN')
    API_HOST = values.Value(default='http://172.17.0.1:8000',environ_name='OCL_API_HOST', environ_prefix=None)
    API_TOKEN = values.Value(default='891b4b17feab99f3ff7e5b5d04ccc5da7aa96da6',environ_name='OCL_API_TOKEN', environ_prefix=None)

class Local(Common):
    """ Local class """
    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = DEBUG

    SECRET_KEY = values.Value(environ_name='SECRET_KEY', environ_prefix='', default='s3owRP0sLI2opDDI6qIgG3iD57')

    ########## INSTALLED_APPS
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('django_extensions',)
    ########## END INSTALLED_APPS

    ########## Mail settings
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = values.Value('django.core.mail.backends.console.EmailBackend')
    ########## End mail settings

    ########## django-debug-toolbar
    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)

    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TEMPLATE_CONTEXT': True,
    }
    ########## end django-debug-toolbar

    ########## Your local stuff: Below this line define 3rd party libary settings

class Qa(Common):
    """ Local class """
    ########### SECRET KEY
    SECRET_KEY = values.SecretValue(environ_prefix="", environ_name="SECRET_KEY")
    ########## END SECRET KEY

    # used to push logs to sentry.io/openconceptlab
    RAVEN_CONFIG = {
        'dsn': os.environ.get('SENTRY_DSN_KEY', ''),
    }

    ########## INSTALLED_APPS
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('django_extensions',)
    ########## END INSTALLED_APPS

    ########## django-debug-toolbar
    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)

    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TEMPLATE_CONTEXT': True,
    }
    ########## end django-debug-toolbar

class Production(Common):
    """ Production class -- the default """
    ########### SECRET KEY
    SECRET_KEY = values.SecretValue(environ_prefix="", environ_name="SECRET_KEY")
    ########## END SECRET KEY

    # used to push logs to sentry.io/openconceptlab
    RAVEN_CONFIG = {
        'dsn': os.environ.get('SENTRY_DSN_KEY', ''),
    }

    ########## INSTALLED_APPS
    INSTALLED_APPS = Common.INSTALLED_APPS
    ########## END INSTALLED_APPS

    ########## django-secure
    INSTALLED_APPS += ("djangosecure", )
    ########## django-debug-toolbar
    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)

    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TEMPLATE_CONTEXT': True,
    }
    ########## end django-debug-toolbar

    # set this to 60 seconds and then to 518400 when you can prove it works
    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_FRAME_DENY = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SESSION_COOKIE_SECURE = values.BooleanValue(False)
    SESSION_COOKIE_HTTPONLY = values.BooleanValue(True)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
    ########## end django-secure

    INSTALLED_APPS += ("gunicorn", )

    ########## STORAGE CONFIGURATION
    # See: http://django-storages.readthedocs.org/en/latest/index.html
#    INSTALLED_APPS += (
#        'storages',
#    )

    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
#    STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
#    AWS_ACCESS_KEY_ID = values.SecretValue()
#    AWS_SECRET_ACCESS_KEY = values.SecretValue()
#    AWS_STORAGE_BUCKET_NAME = values.SecretValue()
#    AWS_AUTO_CREATE_BUCKET = True
#    AWS_QUERYSTRING_AUTH = False

    # see: https://github.com/antonagestam/collectfast
#    AWS_PRELOAD_METADATA = True
#    INSTALLED_APPS += ("collectfast", )

    # AWS cache settings, don't change unless you know what you're doing:
#    AWS_EXPIREY = 60 * 60 * 24 * 7
#    AWS_HEADERS = {
#        'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIREY,
#            AWS_EXPIREY)
#    }

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
#    STATIC_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
    ########## END STORAGE CONFIGURATION

    ########## TEMPLATE CONFIGURATION

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )
    ########## END TEMPLATE CONFIGURATION

    ########## CACHING
    # Only do this here because thanks to django-pylibmc-sasl and pylibmc
    # memcacheify is painful to install on windows.
#    CACHES = values.CacheURLValue(default="memcached://127.0.0.1:11211")
    ########## END CACHING


class Staging(Production):
    ########## INSTALLED_APPS

    INSTALLED_APPS = Common.INSTALLED_APPS

    ########## END INSTALLED_APPS

class Demo(Production):
    pass
