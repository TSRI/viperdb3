from fabric.api import *

def manage(cmd):
    local('python viperdb/manage.py %s' % (cmd))

