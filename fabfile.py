from fabric.api import *
import os.path
import inspect, os
ROOT_PATH = os.path.dirname(inspect.getfile(inspect.currentframe()))

def install():
    local('python bootstrap.py')

def run():
    local('python viperdb/manage.py syncdb --noinput')
    local('python viperdb/manage.py collectstatic --noinput')
    serve()

def manage(cmd):
    local('python viperdb/manage.py %s' % (cmd))

def run_remote():
    with prefix('export DJANGO_RUN_ENV=remote'):
        run()

def shell_remote():
    with prefix('export DJANGO_RUN_ENV=remote'):
        shell()

def serve():
    with lcd(os.path.join(ROOT_PATH, 'viperdb')):
        print os.path.join(ROOT_PATH, 'viperdb')
        LOGFILE = '/var/log/gunicorn/viperdb.log' 
        local('gunicorn_django -w 5 -b viperdb2.scripps.edu:8080 --log-level=debug --log-file='+LOGFILE)

