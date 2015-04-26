from fabric.api import *
import fabric.contrib.project as project
import os
import sys
import SimpleHTTPServer
import SocketServer

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path


def bootstrap():
    local('pip install pelican markdown ghp-import')


def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))


def build():
    local('pelican -s pelicanconf.py')


def rebuild():
    clean()
    build()


def regenerate():
    local('pelican -r -s pelicanconf.py')


def serve():
    os.chdir(env.deploy_path)

    PORT = 8000
    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT), SimpleHTTPServer.SimpleHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()


def reserve():
    build()
    serve()


def preview():
    local('pelican -s publishconf.py')


def publish():
    build()
    local('git checkout gh-pages')
    if not env.deploy_path:
        return
    local('rm -f /tmp/{deploy_path} && mv {deploy_path} /tmp/'.format(**env))
    local('rm -rf *')
    local('mv /tmp/{deploy_path}/* ./'.format(**env))
    local('git add .')
    local('git commit -m $(date)')
    local('git push')
    local('git checkout master')
