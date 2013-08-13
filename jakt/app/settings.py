# coding=utf-8
# Django settings
import os, sys, warnings, dj_database_url, djcelery
from django.core.exceptions import ImproperlyConfigured

def set_from_dict (d, *args):
    new = {}
    for k in args:
        if d.get(k, None) is not None:
            new[k] = d.get(k)
    globals().update(new)

# INTERNAL_IPS = ("127.0.0.1", "0.0.0.0",)
class AllIps ():
    def __init__ (self):
        pass
    def __contains__ (self, ip):
        return True
INTERNAL_IPS = AllIps()


# Switch out the user model
AUTH_USER_MODEL = 'supervisor.User'

DEBUG = False
if os.environ.get("DEBUG", None) is not None:
    DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOW_SIGNUP = True
if os.environ.get("ALLOW_SIGNUP", True) is not True:
    ALLOW_SIGNUP = False

BUGSNAG = {
    "api_key": os.environ.get("BUGSNAG_KEY", None),
    "project_root": os.path.abspath(""),
    "notify_release_stages" : ["production", "staging"],
    "release_stage" : os.environ.get("BUGSNAG_STAGE", "production")
}

CACHES = {
    'default': {
        'BACKEND': os.environ.get("CACHE_BACKEND", 'django.core.cache.backends.locmem.LocMemCache'),
        'LOCATION': os.environ.get("CACHE_LOCATION", 'unique-snowflake')
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

ADMINS = (
    ('JAKT', 'general@byjakt.com'),
)
MANAGERS = ADMINS

# Singly stuff
SINGLY_CLIENT_ID = os.environ.get("SINGLY_CLIENT_ID")
SINGLY_CLIENT_SECRET = os.environ.get("SINGLY_CLIENT_SECRET")
SINGLY_URL = os.environ.get("SINGLY_URL")

TWITTER_KEY = os.environ.get("TWITTER_KEY")
TWITTER_SECRET = os.environ.get("TWITTER_SECRET")

# Email
set_from_dict(os.environ, "EMAIL_BACKEND", "EMAIL_HOST", "SENDGRID_USERNAME", "SENDGRID_PASSWORD", "EMAIL_PORT")
if os.environ.get("EMAIL_PORT"):
    EMAIL_USE_TLS = True

SERVER_EMAIL = "django@localhost"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

if os.environ.get("DATABASE_URL", None):
    DATABASES['default'] = dj_database_url.config()

# Setup celery
BROKER_BACKEND = "django"
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_DISABLE_RATE_LIMITS = True
djcelery.setup_loader()

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [ "0.0.0.0:9002" ]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = os.environ.get("STATIC_URL", "/static/")
if os.environ.get("STATICFILES_STORAGE"):
    STATICFILES_STORAGE = os.environ.get("STATICFILES_STORAGE")

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath("static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = "hjfp(&zi@2c_6$$!i79ao05mlg!k0y%$e-fzjk^&*dda4sallq9-0uzb-^@z-7(*!5l0+5&it09"
if not DEBUG and not SECRET_KEY:
    raise ImproperlyConfigured("No secret key set for new project.")
elif not SECRET_KEY:
    warnings.warn("Your secret key isn't set yet. DON'T YOU DARE IGNORE THIS.")
    SECRET_KEY = 'Fix this'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'app.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'app.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath("templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'south',
    'djcelery',
    'kombu.transport.django',
    'supervisor',
    'product',
    'frontend',
    'app',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters' : {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console' : {
            'level' : 'DEBUG',
            'class' : 'logging.StreamHandler',
            'formatter' : 'simple',
            'stream' : sys.stdout
        }
    },
    'loggers': {
        '' : {
            'handlers' : ['console'],
            'level' : 'DEBUG',
            'propagate' : True
        },
        'product' : {
            'handlers' : [ 'console' ],
            'level' : 'DEBUG',
            'propagate' : True
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}