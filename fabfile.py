from fabric.api import *
from signal import SIGHUP
import os
import sys
import SimpleHTTPServer
import SocketServer

env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path


@task
def bootstrap():
    local('pip install pelican markdown ghp-import yaml')


@task(alias='clean')
def clean_():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))


@task
def build(clean=False, watch=False, env=None):
    if clean:
        clean_()
    tpl = 'CONFIG={env} pelican {watch} -s pelicanconf.py'
    local(tpl.format(env=env, watch='-r' if watch else ''))


@task
def serve():
    os.chdir(env.deploy_path)

    PORT = 8000

    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT), SimpleHTTPServer.SimpleHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()


@task
def develop():
    pid = os.fork()
    if not pid:
        return serve()
    else:
        try:
            build(watch=True)
        except KeyboardInterrupt:
            os.kill(pid, SIGHUP)
            sys.exit()


@task
def preview():
    build(env='production')


@task
def publish():
    preview()
    local('ghp-import {deploy_path}'.format(**env))
    local('git push origin gh-pages')
