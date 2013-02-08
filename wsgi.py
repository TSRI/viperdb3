import os,sys
import django.core.handlers.wsgi
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'
application = django.core.handlers.wsgi.WSGIHandler()