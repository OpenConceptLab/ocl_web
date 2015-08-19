"""
Deployment script for OCL WEB and server setup for both OCL Web and api

Always set environment first using one of the environment commands: fab [env] [command].
For example:
    fab dev deploy
    fab staging release_api_app
    fab production release_web_app

Steps to setup a new server (see build_new_server() for the full list)
    - install_root_key
    - add_deploy_user
    - common_install
    - setup_environment
    - setup_solr
    - setup_mongo
    - setup_postgres
    - setup_supervisor (without keys)
    - build_api_app (this will update supervisor)
    - build_web_app
    - setup_nginx

For each new code release:
    - release_web_app
    - release_api_app

To entirely rebuild the Solr index based on the mongo data:
    - rebuild_index

Server administration commands:
    - restart_web
    - restart_api

Security: Note that all access is setup to user your SSH key. There is only a password for
root, which you have from the initial server build.
"""
from __future__ import with_statement
import os
from time import sleep
import random
import string
import re
from os.path import join, abspath, dirname

from fabric.api import local, run, cd, task, put, settings, require
from fabric.context_managers import prefix
from fabric.operations import sudo, prompt
from fabric.state import env
from fabric.utils import fastprint
from fabric.contrib import files
from fabric.colors import blue, yellow


BACKUP_DIR = '/var/backups/ocl'
CHECKOUT_DIR = '/var/tmp'

#env.user = os.environ['FAB_USER']
#env.password = os.environ['FAB_PASSWORD']
#env.hosts = [os.environ['OCL_WEB_HOST']]



## ENVIRONMENT COMMANDS
## Use as first command to set the environment for all subsequent commands

@task
def dev():
    """
    Put as the first task on the command line to select dev environment.
    For example: fab dev release_web_app
    Put in this task all the environment specific variables and settings.
    """
    env.hosts = ['dev.openconceptlab.com', ]
    env.user = 'deploy'
    env.web_domain = 'dev.openconceptlab.com'
    env.api_domain = 'api.dev.openconceptlab.com'
    env.OCL_API_TOKEN = os.environ.get('OCL_API_TOKEN')
    env.OCL_ANON_API_TOKEN = os.environ.get('OCL_ANON_API_TOKEN')
    env.random_string = _random_string(32)

    # which sites.json file to load the django site object from.
    env.site_spec = 'dev'

    env.AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    env.AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    env.AWS_STORAGE_BUCKET_NAME = 'ocl-source-export-development'

@task
def staging():
    """
    Put as the first task on the command line to select staging environment.
    """
    env.hosts = ['staging.openconceptlab.com', ]
    env.user = 'deploy'
    env.web_domain = 'staging.openconceptlab.com'
    env.api_domain = 'api.staging.openconceptlab.com'
    env.OCL_API_TOKEN = os.environ.get('OCL_API_TOKEN')
    env.OCL_ANON_API_TOKEN = os.environ.get('OCL_ANON_API_TOKEN')
    env.random_string = _random_string(32)
    env.site_spec = 'stage'
    env.AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    env.AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    env.AWS_STORAGE_BUCKET_NAME = 'ocl-source-export-staging'

@task
def production():
    """
    Put as the first task on the command line to select production environment.
    """
    env.hosts = ['www.openconceptlab.com', ]
    env.user = 'deploy'
    env.site_spec = 'prod'
    env.web_domain = 'www.openconceptlab.com'
    env.api_domain = 'api.openconceptlab.com'
    env.OCL_API_TOKEN = 'dummy'
    env.OCL_ANON_API_TOKEN = 'dummy'
    env.random_string = _random_string(32)
    env.AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    env.AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    env.AWS_STORAGE_BUCKET_NAME = 'ocl-source-export-production'



## HELPER FUNCTIONS

def _read_key_file(key_file):
    """ Helper function to read user's public key """
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
    path = dirname(abspath(__file__))
    path = join(path, 'conf', file_name)
    return path

def _random_string(number_chars):
    """ Generate a random string for settings.
    """
    return ''.join(random.sample(string.ascii_uppercase +
                                 string.ascii_lowercase + string.digits, number_chars))

@task
def test_local():
    """ For OCL_API, from old fabfile -- TO TEST THAT ENVIRONMENT IS SETUP """
    local("./manage.py test users")
    local("./manage.py test orgs")
    local("./manage.py test sources")
    local("./manage.py test collection")
    local("./manage.py test concepts")
    local("./manage.py test mappings")

def build_app(app_name, repo_name=None, no_git=False):
    """ Helper for building a django App environment, virtualenv source code etc.
    """

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

def create_api_database():
    """ Helper to create the API mongo database """
    with cd('/opt/deploy/ocl_api/ocl'):
        with prefix('source /opt/virtualenvs/ocl_api/bin/activate'):
            with prefix('export DJANGO_CONFIGURATION="Production"'):
                with prefix('export DJANGO_SECRET_KEY="blah"'):

                    print yellow('creating API database...')
                    # no super user
                    run('./manage.py syncdb --noinput')
                    put(_conf_path('mongo_setup.js'), '~/mongo_setup.js')
                    run('mongo ocl ~/mongo_setup.js')

    # now start the server so that we can create base users
    print yellow('Start up partial API server...')
    run('supervisorctl start ocl_api')

    with cd('/opt/deploy/ocl_api/ocl'):
        with prefix('source /opt/virtualenvs/ocl_api/bin/activate'):
            with prefix('export DJANGO_CONFIGURATION="Production"'):
                with prefix('export DJANGO_SECRET_KEY="blah"'):

                    print yellow('creating internal users: admin and anon ...')
                    run('./manage.py create_tokens --create --password password')

    # now grab the token for the web config
    print yellow('Put tokens into WEB app config...')
    setup_supervisor()
    run('supervisorctl reread')
    run('supervisorctl update')
    # update shell env setup file with new tokens
    files.upload_template(_conf_path(
        'shell_prep.sh'), '~/shell_prep.sh', env)

    # create sysadmin user
    with prefix('source /opt/virtualenvs/ocl_web/bin/activate'):
        print yellow('creating sysadmin user...')
        run('source ~/shell_prep.sh;/opt/deploy/ocl_web/ocl_web/manage.py create_sysadmin')

def release(app_name, do_pip):
    """ Release latest source and dependent files and packages for the named app """
    with cd('/opt/deploy/%s' % app_name):
        fastprint('releasing latest source files')
        run('git pull')
        if do_pip:
            with prefix('source /opt/virtualenvs/%s/bin/activate' % app_name):
                run("pip install -r requirements.txt")



## SERVER SETUP COMMANDS

@task
def install_root_key():
    """Install your SSH key for root. One time task.
    """
    with settings(user='root'):
        print yellow('setting up SSH for root')
        ssh_path = '/root/.ssh'
        if not files.exists(ssh_path, verbose=True):
            run('mkdir %s' % ssh_path)
            run('chmod 700 %s' % ssh_path)
        key_text = _read_key_file('~/.ssh/id_rsa.pub')
        files.append('%s/authorized_keys' % ssh_path, key_text)

@task
def add_deploy_user():
    """Create the deploy user account, one time task.

    The deploy user is used for almost all processes.
    Your SSH key is pushed so that you can login via ssh keys.
    """
    username = 'deploy'
    with settings(user='root'):

        # Create the user, no password
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
    """Basic one-time setup for common packages for ubuntu servers.

    Currently DB stuff and web stuff are listed together. Could split
    them if we run separate servers.
    """
    print yellow('common_install...')
    sudo('apt-get update')

    # user console tools
    sudo("apt-get -y -q install emacs23-nox unzip lsof byobu httpie")

    # application libraries
    sudo("apt-get -y -q  install python-pip git-core")
    sudo('apt-get -y -q install build-essential python-dev')
    sudo("apt-get -y -q  install libpq-dev")

    sudo("apt-get -y -q install supervisor")
    sudo("pip install virtualenv")

    # web
    # memcached
    sudo('apt-get -y -q install nginx')

    # database
    # if you don't want database, at least install the client
    # sudo("apt-get -y -q install postgresql-client")
    sudo("apt-get -y -q install postgresql postgresql-contrib")
    # Could use redis for celery but not yet
    # sudo("apt-get -q install redis-server")

@task
def setup_supervisor():
    """Setup supervisor daemon for running OCL processes.

    One of the key function is to put the API tokens required in the
    environment for Web server.
     """

    # first time this will fail because we have a chicken and egg
    # situation, we need the API server to get the tokens, but
    # we need supervisor to run the API server
    auth_token, anon_token = get_api_tokens()
    if auth_token is not None and anon_token is not None:
        env.OCL_API_TOKEN = auth_token
        env.OCL_ANON_API_TOKEN = anon_token
    files.upload_template(_conf_path('ocl_supervisor.conf'),
                          '/etc/supervisor/conf.d', env, use_sudo=True)
    put(_conf_path('supervisord.conf'), '/etc/supervisor', use_sudo=True)
    # restart to run as deploy
    sudo('/etc/init.d/supervisor restart')

@task
def setup_nginx():
    """Setup nginx.

    This can be re-run to update the application configuration via
    the ocl_nginx.conf.
    """
    with settings(warn_only=True):
        sudo('unlink /etc/nginx/sites-enabled/default')

    files.upload_template(_conf_path('ocl_nginx.conf'),
                          '/etc/nginx/sites-available/ocl', env, use_sudo=True)

    with settings(warn_only=True):
        sudo('ln -s /etc/nginx/sites-available/ocl /etc/nginx/sites-enabled/ocl')

    sudo('/etc/init.d/nginx restart')

@task
def setup_environment():
    """Create OCL directories and files.
    """
    for directory in ['/opt/virtualenvs', '/opt/deploy']:
        if not files.exists(directory):
            print yellow('Creating directory %s...' % directory)
            sudo('mkdir %s' % directory)
            sudo('chown deploy:deploy %s' % directory)

    # all logs go to /var/log/ocl subdirectories.
    if not files.exists('/var/log/ocl'):
        sudo('mkdir /var/log/ocl')
        sudo('chown deploy:deploy /var/log/ocl')

    # This backup dir is used by the current API server deployment
    # process.
    if not files.exists(BACKUP_DIR):
        sudo('mkdir -p %s' % BACKUP_DIR)
        sudo('chown deploy:deploy %s' % BACKUP_DIR)

    # A few shell aliases that PK likes...
    put(_conf_path('ocl_aliases'), '~/.bash_aliases')
    put(_conf_path('tmux.conf'), '~/.tmux.conf')

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
    sudo('sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10')
    put(_conf_path('mongo.apt'), '/etc/apt/sources.list.d/mongodb.list', use_sudo=True)
    sudo('apt-get update')
    sudo('apt-get install -y -q mongodb-org')

@task
def setup_solr():
    """ Setup solr server """
    sudo('apt-get -y -q install openjdk-7-jdk')

    ## no need?
    ## sudo('mkdir /usr/java')
    ## sudo('ln -s /usr/lib/jvm/java-7-openjdk-amd64 /usr/java/default')

    with cd('/opt'):
        sudo('wget http://archive.apache.org/dist/lucene/solr/4.9.1/solr-4.9.1.tgz')
        sudo('tar -xvf solr-4.9.1.tgz')
        sudo('cp -R solr-4.9.1/example /opt/solr')
        sudo('chown -R deploy:deploy /opt/solr')

    with settings(user='root'):
        put(_conf_path('default.jetty'), '/etc/default/jetty')
        put(_conf_path('jetty'), '/etc/init.d')
        run('chmod a+x /etc/init.d/jetty')

    if not files.exists('/var/log/solr'):
        sudo('mkdir /var/log/solr')
        sudo('chown deploy:deploy /var/log/solr')

    with cd('/opt/deploy/'):
        print yellow('creating project root for %s' % 'solr')
        run('mkdir %s' % 'solr')

@task
def build_web_app():
    """ Build the web app, one time task. """
    build_app('ocl_web')
    release_web_app(do_pip=True)

    # setup DB, no super user.
    with cd('/opt/deploy/ocl_web'):
        with prefix('source /opt/virtualenvs/ocl_web/bin/activate'):
            with prefix('export DJANGO_CONFIGURATION="Production"'):
                with prefix('export DJANGO_SECRET_KEY="blah"'):
                    print yellow('creating WEB database...')
                    run('ocl_web/manage.py syncdb --noinput --migrate')

@task
def build_api_app():
    """ Build the API app, one time task. """
    build_app('ocl_api', repo_name='oclapi', no_git=True)
    checkout_api_app(do_pip=True)
    create_api_database()



## OTHER COMMANDS

@task
def get_api_tokens():
    """
    Get the API_AUTH_TOKEN and ANON_TOKEN from the API server directly

    return tuple or None:
        (api_token, anon_token)
    """
    api_token = anon_token = None
    if not files.exists('/opt/deploy/ocl_api/ocl'):
        return (None, None)

    with cd('/opt/deploy/ocl_api/ocl'):
        with prefix("source /opt/virtualenvs/ocl_api/bin/activate"):
            with prefix('export DJANGO_CONFIGURATION="Production"'):
                with prefix('export DJANGO_SECRET_KEY="blah"'):

                    print yellow('Getting AUTH Tokens')
                    data = run('./manage.py create_tokens')
                    # get back two lines in export form:
                    #    export OCL_API_TOKEN='NNN'
                    #    export OCL_ANON_API_TOKEN='NNNN'
                    # sometimes we get into a chicken and egg situation
                    # with a bad server image. So handle error cases
                    lines = data.split('\n')
                    if len(lines) < 2:
                        return (None, None)

                    r = re.search("export OCL_API_TOKEN='(\w+)'", lines[0])
                    if r is None:
                        return (None, None)
                    api_token = r.group(1)
                    r = re.search("export OCL_ANON_API_TOKEN='(\w+)'", lines[1])
                    if r is None:
                        return (None, None)
                    anon_token = r.group(1)

                    print 'API Token: %s,  Anon Token: %s' % (api_token, anon_token)
                    return (api_token, anon_token)

@task
def load_site_name():
    """
    Set the global site object value in the web server, used in outbound emails.
    """
    with cd('/opt/deploy/ocl_web'):
        with prefix('source /opt/virtualenvs/ocl_web/bin/activate'):
            with prefix('export DJANGO_CONFIGURATION="Production"'):
                with prefix('export DJANGO_SECRET_KEY="blah"'):
                    print yellow('setting site name...')
                    run('ocl_web/manage.py loaddata ocl_web/config/sites.%s.json' % env.site_spec)

@task
def checkout_api_app(do_pip=False):
    """ Get latest API server software.
        This is normally done as part of release task's git clone.

        This process is different from the web server process because
        it uses a "git cone, then copy the source files to runtime"
        method for the release instead of directly pulling into the
        run time.
    """
    with cd('/var/tmp'):
        print blue('pulling new code...')
        sudo('/etc/init.d/jetty stop')
        run("rm -rf oclapi")
        run("git clone https://github.com/OpenConceptLab/oclapi.git")

        print blue('deleting old code...')
        run('rm -rf /opt/deploy/ocl_api/ocl')
        run('rm -rf /opt/deploy/solr/collection1')

        print blue('copying new code...')
        run("cp -r oclapi/django-nonrel/ocl /opt/deploy/ocl_api")
        run('mkdir -p /opt/deploy/solr/collection1')
        run("cp -r oclapi/solr/collection1/conf /opt/deploy/solr/collection1")

    with cd("/opt/deploy/ocl_api/ocl"):
        # there is no need for this, settings.py.eploy is actually wrong?
        # run("cp settings.py.deploy settings.py")
        with prefix("source /opt/virtualenvs/ocl_api/bin/activate"):
            with prefix('export DJANGO_CONFIGURATION="Production"'):
                with prefix('export DJANGO_SECRET_KEY="blah"'):
                    # this is really slow because it pull down django-norel
                    if do_pip:
                        run("pip install -r requirements.txt")
                    run('./manage.py build_solr_schema > ' +
                        '/opt/deploy/solr/collection1/conf/schema.xml')
    sudo('/etc/init.d/jetty start')

@task
def api_backup():
    """ Backup API server environment """
    if not files.exists(BACKUP_DIR):
        sudo('mkdir -p %s' % BACKUP_DIR)
        sudo('chown deploy:deploy %s' % BACKUP_DIR)

    with cd('/opt/deploy/ocl_api'):
        run("tar -czvf ocl_api_`date +%Y%m%d`.tgz ocl_api solr/collection1/conf")
        run("mv ocl_api_*.tgz %s" % BACKUP_DIR)

@task
def release_api_app(do_pip=False):
    """ Release latest API server software.
    """
    run('/etc/init.d/jetty stop')
    run('supervisorctl stop ocl_api')
    run('supervisorctl stop celery')
    sleep(5)

    release('ocl_api', do_pip)
    # However, the ocl directory structure in git is not yet aligned with
    # runtime. Hence this symlink
    with cd("/opt/deploy/ocl_api"):
        run('ln -s django-nonrel/ocl ocl')

    # Startup celery and the ocl_api web app
    run('supervisorctl start ocl_api')
    run('supervisorctl start celery')

    return

@task
def release_web_app(do_pip=False):
    """ Release latest version of WEB application """
    release('ocl_web', do_pip)
    run('supervisorctl restart ocl_web')

@task
def clear_databases():
    """ Clear out all databases. This is very destructive, only useful for testing! """

    require('hosts', provided_by=['dev', 'staging', 'production'])
    ans = prompt('This will completely wipe out the database. Are you sure (YES/no)?')
    if ans != 'YES':
        print yellow('Glad you were just kidding.')
        return

    ans = prompt(yellow('%s' % env.hosts[0]) + ' database will be wiped. Are you sure (YES/no)?')
    if ans != 'YES':
        print "Didn't think so."
        return

    run('supervisorctl stop all')
    print yellow('Recreate WEB database')
    run('dropdb  ocl_web')
    run('createdb -O deploy ocl_web')
    # setup DB
    with prefix('source /opt/virtualenvs/ocl_web/bin/activate'):
        with prefix('export DJANGO_CONFIGURATION="Production"'):
            with prefix('export DJANGO_SECRET_KEY="blah"'):
                print yellow('creating WEB database...')
                run('/opt/deploy/ocl_web/ocl_web/manage.py syncdb --noinput --migrate')

    print yellow('Recreate API database')
    run('echo -e "use ocl \n db.dropDatabase();" | mongo')
    create_api_database()

@task
def load_orgs_and_sources():
    """
    Load standard set of organization and source
    """
    with prefix('source /opt/virtualenvs/ocl_web/bin/activate'):
        with cd('/opt/deploy/ocl_web/ocl_web'):
            print yellow('creating basic ORGS and SOURCES...')
            run('source ~/shell_prep.sh;/opt/deploy/ocl_web/ocl_web/manage.py ' +
                'create_org --username=sysadmin --csv=fixtures/orgs.csv')
            run('source ~/shell_prep.sh;/opt/deploy/ocl_web/ocl_web/manage.py ' +
                'create_source --username=sysadmin --csv=fixtures/ocl_sources.csv')

@task
def rebuild_index():
    """ Rebuild search index """
    with prefix("source /opt/virtualenvs/ocl_api/bin/activate"):
        with prefix('export DJANGO_CONFIGURATION="Production"'):
            sudo('/etc/init.d/jetty restart')
            sleep(5)
            run("/opt/deploy/ocl_api/ocl/manage.py rebuild_index")

@task
def full_restart():
    """ Restart everything """
    sudo('/etc/init.d/apache2 stop')
    sudo('/etc/init.d/nginx restart')
    sudo('/etc/init.d/supervisor restart')
    sudo('/etc/init.d/mongod restart')
    sudo('/etc/init.d/jetty restart')

@task
def build_new_server():
    """ Build a brand new server from scratch. """
    require('hosts', provided_by=['dev', 'staging', 'production'])
    ans = prompt('This will completely wipe out the server. Are you sure (YES/no)?')
    if ans != 'YES':
        print yellow('Glad you were just kidding.')
        return

    ans = prompt(yellow('%s' % env.hosts[0]) + ' will be wiped and rebuilt. Are you sure (YES/no)?')
    if ans != 'YES':
        print "Didn't think so."
        return

    env.keepalive = 30

    install_root_key()
    add_deploy_user()
    common_install()
    setup_environment()
    setup_solr()
    setup_mongo()
    setup_postgres()
    setup_supervisor()
    build_api_app()
    build_web_app()
    setup_nginx()
    full_restart()

@task
def restart_web():
    """ Restart OCL WEB server """
    run('supervisorctl restart ocl_web')

@task
def restart_api():
    """ Restart OCL API server """
    run('supervisorctl restart ocl_api')

@task
def status():
    """ Displays supervisorctl status """
    run('supervisorctl status')

@task
def blah():
    """ Helper to create the API mongo database """
    with cd('/opt/deploy/ocl_api/ocl'):
        with prefix('source /opt/virtualenvs/ocl_api/bin/activate'):
            with prefix('export DJANGO_CONFIGURATION="Production"'):
                with prefix('export DJANGO_SECRET_KEY="blah"'):

                    print yellow('preping environment due to changes...')
                    auth_token, anon_token = get_api_tokens()
                    if auth_token is not None and anon_token is not None:
                        env.OCL_API_TOKEN = auth_token
                        env.OCL_ANON_API_TOKEN = anon_token

                    files.upload_template(
                        _conf_path('shell_prep.sh'), '~/shell_prep.sh', env)

@task
def fix_solr():
    """ Fix solr
        work in progress
    """
    with cd('/var/tmp'):
        print blue('pulling new code...')
        sudo('/etc/init.d/jetty stop')
        sleep(5)
        # run('rm -rf /opt/deploy/solr/collection1')

        print blue('copying new code...')
        # run('mkdir -p /opt/deploy/solr/collection1')
        # run("cp -r oclapi/solr/collection1/conf /opt/deploy/solr/collection1")

    with cd("/opt/deploy/ocl_api/ocl"):
        # there is no need for this, settings.py.eploy is actually wrong?
        # run("cp settings.py.deploy settings.py")
        with prefix('source /opt/virtualenvs/ocl_api/bin/activate'):
            with prefix('export DJANGO_CONFIGURATION="Production"'):
                with prefix('export DJANGO_SECRET_KEY="blah"'):
                    # this is really slow because it pull down django-norel
                    run('./manage.py build_solr_schema > ' +
                        '/opt/deploy/solr/collection1/conf/schema.xml')
    sleep(5)
    sudo('/etc/init.d/jetty start')
