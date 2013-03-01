from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

# Django settings for viperdb project.
from utils import project
import os

# Celery configuration
import djcelery
djcelery.setup_loader()

BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

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
        'USER': os.getenv("VIPERDB_USERNAME"),
        'PASSWORD': os.getenv("VIPERDB_PASSWORD"),
        'HOST': os.getenv("VIPERDB_HOST"),                      
        'PORT': os.getenv("VIPERDB_PORT"),
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
STATIC_ROOT = project('static/')

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
    project('static_files/'),
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

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (project('static_files/templates/'),)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'suit',
    'django.contrib.admin',
    'django_extensions',
    'south',
    'adminplus',
    'viperdb',
    'djcelery',
    'api',
    'gunicorn',
    'debug_toolbar',
    'djsupervisor',
    'pipeline',
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

SUIT_CONFIG = {
    'SHOW_REQUIRED_ASTERISK': True,
    'ADMIN_NAME': 'VIPERdb'
}

# django-pipeline settings
PIPELINE_JS = {
    'main': {
        'source_filenames': (
            'vendor/js/jquery.min.js',
            'vendor/js/underscore-min.js',
        ),
        'output_filename': 'js/main.js',
    },
    'add_entry': {
        'source_filenames': (
            'vendor/js/jquery.formset.min.js',
        ),
        'output_filename': 'js/add_entry.js',
        'variant': 'datauri',
    },
    'step_one': {
        'source_filenames': ('js/virus/step-one.coffee',),
        'output_filename': 'js/step-one.js',
    },
    'step_two': {
        'source_filenames': ('js/virus/step-two.coffee',),
        'output_filename': 'js/step-two.js',
    },
    'graph': {
        'source_filenames': (
            'vendor/js/d3.v2.min.js',
            'vendor/js/d3.tip.min.js',
            'js/virus/graph.coffee',
            'js/virus/scatter-graph.coffee',
        ),
        'output_filename': 'js/graph.js',
        'variant': 'datauri',
    },
    'images': {
        'source_filenames': (
            'vendor/js/fancyBox/jquery.fancybox.js',
            'vendor/js/fancyBox/helpers/jquery.fancybox-thumbs.js',
            'vendor/js/carouFredSel-6.2.0/jquery.carouFredSel-6.2.0.js',
            'js/virus/info.coffee',

        ),
        'output_filename': 'js/images.js',
        'variant': 'datauri',
    },
    'gallery_maker': {
        'source_filenames': (
            'vendor/js/isotope/jquery.isotope.min.js',
            'vendor/js/fresco/fresco.js',
            'js/gallery_maker/gallery-maker.js',
        ),
        'output_filename': 'js/gallery-maker.js',
        'variant': 'daturi',
    },
}

PIPELINE_CSS = {
    'main': {'source_filenames': ('sass/main.sass',)},
    'graph': {
        'source_filenames': (
            'sass/graph.sass',
            'sass/scatter-graph.sass',
        ),
        'output_filename': 'stylesheets/graph.css',
        'variant': 'datauri',
    },
    'images': {
        'source_filenames': (
            'vendor/css/fancyBox/jquery.fancybox.css',
            'vendor/css/fancyBox/jquery.fancybox-buttons.css',
            'vendor/css/fancyBox/jquery.fancybox-thumbs.css',
            'vendor/css/isotope.css',
            'vendor/css/fresco/fresco.css'
        ),
        'output_filename': 'stylesheets/fancybox.css',
        'variant': 'datauri',
    },
}
PIPELINE_COMPILERS = (
    'pipeline.compilers.coffee.CoffeeScriptCompiler',    
    'pipeline_compass.compass.CompassCompiler',
)
PIPELINE_COFFEE_SCRIPT_BINARY = '/usr/local/bin/coffee'
PIPELINE_COMPASS_BINARY = '/usr/local/bin/compass'
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None
STATICFILES_STORAGE = "pipeline.storage.PipelineCachedStorage"
PIPELINE_DISABLE_WRAPPER = True

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
