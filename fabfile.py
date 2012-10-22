from fabric.api import *

env.ve = "~/.env/bin/"
env.activate = "source ~/.env/bin/activate"
env.hosts = ['viperdb@127.0.0.1']

def virtualenv(command):
    "Run a command within a virtualenv"
    return env.ve + command

def manage(cmd):
    local('python app/manage.py %s' % (cmd))

def bootstrap():
    bootstrap_server()

def bootstrap_server(_local=True):
    with cd("viperdb3"):
        f = local if _local else sudo 
        f(virtualenv("pip install -r requirements.txt"))

def serve():
    with cd('viperdb'):
        manage('runserver')
    



