from fabric.api import *
import envoy

env.activate = "source /export/viperdb/.virtualenvs/viperdb/bin/activate"
env.hosts = ["localhost"]
env.f = sudo

def virtualenv(command):
    """Run a command within a virtualenv"""
    with cd("viperdb3"):
        env.f("%s && %s" % (env.activate, command))

def manage(cmd):
    virtualenv('honcho run python app/manage.py %s' % (cmd))

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

        manage("syncdb")
        manage("migrate")

