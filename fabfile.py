"""
    Deployment script for OCL WEB and server setup for both OCL Web and api

    Runs with first task = environment, e.g.
    fab dev deploy
    fab staging deploy

    steps:
    These are one time:
    1. add_deploy_user
    2. common_install
    3. setup_environment
    4. build_web_app
    5. setup_supervisor
    6. setup_nginx

    These are for each new release:
    4. release_web_app
"""
from __future__ import with_statement
import os
import random
import string
from os.path import join, abspath, dirname

from fabric.api import local, run, cd, task, put
from fabric.api import settings
from fabric.context_managers import prefix
from fabric.operations import sudo
from fabric.state import env
from fabric.utils import fastprint
from fabric.contrib import files
from fabric.colors import blue, green


BACKUP_DIR = '/var/backups/ocl'
CHECKOUT_DIR = '/var/tmp'


#env.user = os.environ['FAB_USER']
#env.password = os.environ['FAB_PASSWORD']
#env.hosts = [os.environ['OCL_WEB_HOST']]


@task
def dev():
    """
    Make this the first task when calling fab to
    perform operations on dev machine.
    """
    env.hosts = ['dev.openconceptlab.org', ]
    env.user = 'deploy'
    env.web_domain = 'dev.openconceptlab.com'
    env.api_domain = 'api.dev.openconceptlab.com'
    env.OCL_API_TOKEN = os.environ.get('OCL_API_TOKEN')
    env.OCL_ANON_API_TOKEN = os.environ.get('OCL_ANON_API_TOKEN')
    env.random_string = _random_string(32)


@task
def staging():
    """
    Make this the first task when calling fab to
    perform operations on staging machine.
    """
    env.hosts = ['staging.openconceptlab.org', ]
    env.user = 'deploy'


@task
def test_remote():
    run('pwd;ls')


def hello(name="World"):
    print("Hello %s" % name)


def test_local():
    local("./manage.py test users")
    local("./manage.py test orgs")
    local("./manage.py test sources")
    local("./manage.py test collection")
    local("./manage.py test concepts")
    local("./manage.py test mappings")


def _read_key_file(key_file):
    """ Read user's public key """
    key_file = os.path.expanduser(key_file)
    if not key_file.endswith('pub'):
        raise RuntimeWarning('Trying to push non-public part of key pair')
    with open(key_file) as f:
        return f.read()


def _conf_path(file_name):
    """ Helper to build config template file path for uploading.
        This module will be installed by users into site-packages.
        We need to figure out where the runtime files sit.
    """
    p = dirname(abspath(__file__))
    p = join(p, 'conf', file_name)
    return p


def _random_string(n):
    """ Generate a random string for settings.
    """
    return ''.join(random.sample(string.ascii_uppercase +
                                 string.ascii_lowercase + string.digits, n))


@task
def add_deploy_user():
    """ Run this onces to create the deploy user account, which is used for
        everything else.
    """
    username = 'deploy'
    with settings(user='root'):
        fastprint('adding the %s user account...' % username)
        run('useradd -m -s /bin/bash %s' % username)
        run('adduser %s sudo' % username)

        # Allow this user to sudo without password
        # really should list specific command (the last ALL)
        files.append('/etc/sudoers.d/%s' % username,
                     '%s ALL=(ALL:ALL) NOPASSWD: ALL' % username)

        fastprint('setting up SSH')
        ssh_path = '/home/%s/.ssh' % username
        if not files.exists(ssh_path, verbose=True):
            run('mkdir %s' % ssh_path)
            run('chmod 700 %s' % ssh_path)

            key_text = _read_key_file('~/.ssh/id_rsa.pub')
            files.append('%s/authorized_keys' % ssh_path, key_text)

            run('chown -R %s:%s %s' % (username, username, ssh_path))


@task
def common_install():
    """
    Basic one-time setup for common packages for ubuntu servers.

    Currently DB stuff and web stuff are listed together. Could split
    them if we run separate servers.
    """
    fastprint('common_install...')
    sudo('apt-get update')
    # TODO: Add memcached

    # user console tools
    sudo("apt-get -y -q install emacs23-nox unzip lsof byobu")

    # application libraries
    sudo("apt-get -y -q  install python-pip git-core")
    sudo('apt-get -y -q install build-essential python-dev')
    sudo("apt-get -y -q  install libpq-dev")

    sudo("apt-get -y -q install supervisor")
    sudo("pip install virtualenv")

    # for building dev libraries
#    sudo("apt-get -y -q  install libjpeg62-dev") # images
#    sudo("pip install keyring mercurial_keyring")

    # web
    # memcached
    sudo('apt-get -y -q install nginx')

    # database
    # if you don't want database, at least install the client
    # sudo("apt-get -y -q install postgresql-client")
    sudo("apt-get -y -q install postgresql postgresql-contrib")


@task
def setup_supervisor():
    """ Setup supervisor daemon for controlling python processes """
    files.upload_template(_conf_path('ocl_supervisor.conf'),
                          '/etc/supervisor/conf.d', env, use_sudo=True)
    put(_conf_path('supervisord.conf'), '/etc/supervisor', use_sudo=True)


@task
def setup_nginx():
    """ Setup nginx """
    sudo('unlink /etc/nginx/sites-enabled/default')
    files.upload_template(_conf_path('ocl_nginx.conf'),
                          '/etc/nginx/sites-available/ocl', env, use_sudo=True)
    sudo('ln -s /etc/nginx/sites-available/ocl /etc/nginx/sites-enabled/ocl')


@task
def setup_environment():
    """ create directories and files """
    for d in ['/opt/virtualenvs', '/opt/deploy']:
        if not files.exists(d):
            fastprint('Creating directory %s...' % d)
            sudo('mkdir %s' % d)
            sudo('chown deploy:deploy %s' % d)
    if not files.exists('/var/log/ocl'):
        sudo('mkdir /var/log/ocl')
        sudo('chown deploy:deploy /var/log/ocl')

    if not files.exists(BACKUP_DIR):
        sudo('mkdir -p %s' % BACKUP_DIR)
        sudo('chown deploy:deploy %s' % BACKUP_DIR)

    put(_conf_path('ocl_aliases'), '~/.bash_aliases')


@task
def setup_postgres():
    """ Setup postgres database.
        Give deploy user createdb access to database so that she can
        create test db as well. Also make control easier.
    """

    sudo('createuser --createdb deploy', user='postgres')
    sudo("psql --command=\"ALTER USER deploy with PASSWORD 'deploy';\" ", user='postgres')
    run('createdb -O deploy ocl_web')


@task
def setup_mongo():
    """ Setup mongo database """
#    sudo('sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10')
#    put(_conf_path('mongo.apt'), '/etc/apt/sources.list.d/mongodb.list', use_sudo=True)
    sudo('apt-get update')
    sudo('apt-get install -y mongodb-org')


def build_app(app_name, repo_name=None, no_git=False):
    """ Build a django App """

    with cd('/opt/virtualenvs'):
        fastprint('creating virtualenv for %s' % app_name)
        run('virtualenv %s' % app_name)
    with cd('/opt/deploy/'):
        fastprint('creating project root for %s' % app_name)
        run('mkdir %s' % app_name)

    if no_git:
        return  # just for API because it does not use git directly
    with cd('/opt/deploy/%s' % app_name):
        if repo_name is None:
            repo_name = app_name + '.git'
        run('git clone https://github.com/OpenConceptLab/%s .' % repo_name)


@task
def build_web_app():
    build_app('ocl_web')

    with cd('/opt/deploy/ocl_web'):

        with prefix('source /opt/virtualenvs/ocl_web/bin/activate'):
            with prefix('export DJANGO_CONFIGURATION="Production"'):
                with prefix('export DJANGO_SECRET_KEY="blah"'):
                    print(blue('creating database...'))
                    run('ocl_web/manage.py syncdb --noinput --migrate')


@task
def build_api_app():
    build_app('ocl_api', repo_name='oclapi', no_git=True)
    with cd('/opt/deploy/'):
        print(blue('creating project root for %s' % 'solr'))
        run('mkdir %s' % 'solr')
    return
    with cd('/opt/deploy/ocl_api'):

        with prefix('source /opt/virtualenvs/ocl_api/bin/activate'):
            with prefix('export DJANGO_CONFIGURATION="Production"'):
                with prefix('export DJANGO_SECRET_KEY="blah"'):
                    print(blue('creating database...'))
                    run('xxxx/manage.py syncdb --noinput --migrate')


@task
def api_backup():
    if not files.exists(BACKUP_DIR):
        sudo('mkdir -p %s' % BACKUP_DIR)
        sudo('chown deploy:deploy %s' % BACKUP_DIR)

    with cd('/opt/deploy/ocl_api'):
        run("tar -czvf ocl_api_`date +%Y%m%d`.tgz ocl_api solr/collection1/conf")
        run("mv ocl_api_*.tgz %s" % BACKUP_DIR)
#        run("rm -rf django solr/collection1/conf")


def api_checkout():
    with cd('/var/tmp'):
        run("rm -rf oclapi")
        run("git clone https://github.com/OpenConceptLab/oclapi.git")


@task
def api_provision():
    with cd('/var/tmp'):
        print(blue('pulling new code...'))
        run("rm -rf oclapi")
        run("git clone https://github.com/OpenConceptLab/oclapi.git")

        print(blue('deleting old code...'))
        run('rm -rf /opt/deploy/ocl_api/ocl')
        run('rm -rf /opt/deploy/solor/collection1')

        print(blue('copying new code...'))
        run("cp -r oclapi/django-nonrel/ocl /opt/deploy/ocl_api")
        run("cp -r oclapi/solr/collection1/conf /opt/deploy/solr/collection1")
        return
        sudo("chown -R solr:wheel /opt/deploy/solr")
    with cd("/opt/deploy/ocl_api/ocl"):
        run("cp settings.py.deploy settings.py")
        with prefix("source /opt/virtualenvs/ocl_api/bin/activate"):
            run("pip install -r requirements.txt")
            run("./manage.py test users")
            run("./manage.py test orgs")
            run("./manage.py test sources")
            run("./manage.py test collection")
            run("./manage.py test concepts")
            run("./manage.py build_solr_schema > /opt/deploy/solr/collection1/conf/schema.xml")
            sudo('/etc/init.d/jetty restart')
            run("./manage.py rebuild_index")


def release(app_name):
    """ Release latest source and dependent files and packages for the named app """
    with cd('/opt/deploy/%s' % app_name):
        fastprint('releasing latest source files')
        run('git pull')
        with prefix('source /opt/virtualenvs/%s/bin/activate' % app_name):
            run("pip install -r requirements.txt")


@task
def release_web_app():
    release('ocl_web')


@task
def restart():
    """ Restart OCL WEB server """
    run('supervisorctl restart ocl_web')


@task
def status():
    run('supervisorctl status')


def deploy():
    release()
    restart()
