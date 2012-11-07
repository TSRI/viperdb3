from fabric.api import *

env.activate = "source ~/.env/bin/activate"
env.hosts = ["localhost"]

def virtualenv(command):
    "Run a command within a virtualenv"
    return "%s %s" % (env.activate, command)

def manage(cmd):
    local('python app/manage.py %s' % (cmd))

def bootstrap():
    bootstrap_server()

def bootstrap_server(_local=True):
    with cd("viperdb3"):
        f = sudo
        # f = local if _local else sudo 
        f('gem install bundler --no-ri --no-rdoc')
        f('bundle install')
        f("npm install -g coffee-script")
        f(virtualenv("pip install -r requirements.txt"))

def serve():
    with cd('viperdb'):
        manage('runserver_plus --threaded')
    



