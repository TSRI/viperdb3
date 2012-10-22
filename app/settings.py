# Django settings for viperdb project.
from utils import project
import os

# Celery configuration
import djcelery
djcelery.setup_loader()

RUN_ENV = 'DJANGO_RUN_ENV'

from settings_local import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT

CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("virus.tasks", )

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)   

MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'viperdb',                      
        'USER': DB_USERNAME,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,                      
        'PORT': DB_PORT,
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = project('media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
# MEDIA_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = project('_generated_media') if DEBUG else project('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    project('static_files'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'x%vtygg+uoc5f4eo_dyq$+$c3@!u++kv+(ju2b2ijg+8tqvx%%'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'mediagenerator.middleware.MediaMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
if DEBUG:
    MIDDLEWARE_CLASSES += ('django_pdb.middleware.PdbMiddleware',)

ROOT_URLCONF = 'viperdb.urls'

TEMPLATE_DIRS = (project('static/templates/'),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'viperdb',
    'djcelery',
    'api',
    'gunicorn',
    'django_pdb',
    'mediagenerator',
    'debug_toolbar',
    'djsupervisor'
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

def custom_show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'EXTRA_SIGNALS': [],
    'HIDE_DJANGO_SQL': False,
    'TAG': 'body',
}

MEDIA_DEV_MODE = DEBUG
DEV_MEDIA_URL = '/static/'
PRODUCTION_MEDIA_URL = '/static/'
GENERATED_MEDIA_DIR = '/usr/people/viperdb/website/viperdb/_generated_media/'
GENERATED_MEDIA_NAMES_MODULE =  'viperdb._generated_media_names'
GENERATED_MEDIA_NAMES_FILE = "/usr/people/viperdb/website/viperdb/_generated_media_names.py"
GLOBAL_MEDIA_DIRS = (os.path.join(os.path.dirname(__file__), 'static'),)

MEDIA_BUNDLES = (
    ('main.js',
        'js/jquery.min.js',
        'js/underscore-min.js',
    ),
    ('d3.js', 
        'js/d3.v2.min.js',
        'js/d3.tip.min.js'
    ),
    ('add.js',           'js/jquery.formset.min.js'),
    ('bar-graph.js',     'js/virus/graph.coffee'),
    ('scatter-graph.js', 'js/virus/scatter-graph.coffee'),
    ('phi-psi.js',       'js/virus/phi-psi.coffee'),
    ('step-one.js',      'js/virus/step-one.coffee'),
    ('step-two.js',      'js/virus/step-two.coffee'),
    ('main.css',          'css/main.sass'),
    ('graph.css',         'css/graph.sass'),
    ('scatter-graph.css', 'css/scatter-graph.sass'),
    ('phi-psi.css',       'css/phi-psi.sass'),
)

COPY_MEDIA_FILETYPES = ('gif', 'jpg', 'jpeg', 'png', 'svg', 'svgz', 'html',
                        'ico', 'swf', 'ttf', 'otf', 'eot', 'woff')
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
