from fabric.api import *

ENV_PREFIX = 'workon onesalon.org && '


def runenv(cmd):
    local(ENV_PREFIX + cmd)


@task
def bootstrap():
    local('mkvirtualenv onesalon.org')
    runenv('pip install -r requirements.txt')
