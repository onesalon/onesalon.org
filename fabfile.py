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
    local('pip install pelican markdown ghp-import yaml')


def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))


def build_directory_page():
    import yaml
    directory = yaml.load(open('content/extra/directory.yaml'))
    with open('content/pages/directory.md', 'w') as f:
        f.write('## Directory\n\n')
        for chapter in directory['chapters']:
            f.write('#### [{name}]({link})\n\n'.format(
                name=chapter.get('name', chapter['location']),
                link=chapter['link']
            ))


def build(clean=False, watch=False, env=None):
    if clean:
        clean()
    build_directory_page()
    tpl = 'ENV={env} pelican {watch} -s pelicanconf.py'
    local(tpl.format(env=env, watch='-r' if watch else ''))


def serve():
    os.chdir(env.deploy_path)

    PORT = 8000
    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT), SimpleHTTPServer.SimpleHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()


def develop():
    pid = os.fork()
    if not pid:
        return serve()
    else:
        build(watch=True)


def preview():
    build(env='production')


def publish():
    preview()
    local('ghp-import {deploy_path}'.format(**env))
    local('git push origin gh-pages')
