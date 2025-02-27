#!/usr/bin/python3
"""distributes an archive to your web servers, using the function do_deploy:"""
from os.path import exists
from datetime import datetime
from fabric.api import local, env, put, run

env.hosts = ['3.229.120.108', '44.192.24.108']
env.use_ssh_config = True
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'

def do_pack():
    """Function compresses file"""
    date_time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    path = "versions/web_static_{}.tgz".format(date_time)
    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(path))
    if result.failed:
        return None
    return path


def do_deploy(archive_path):
    """Function to distributes archive to server"""
    if exists(archive_path) is False:
        return False
    file_name = archive_path.split("/")[-1]
    file_noext = file_name.split(".")[0]
    path = "/data/web_static/releases/"
    res = put(archive_path, '/tmp/')
    if res.failed:
        return False
    res = run('mkdir -p {}{}/'.format(path, file_noext))
    if res.failed:
        return False
    res = run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, file_noext))
    if res.failed:
        return False
    res = run('rm /tmp/{}'.format(file_name))
    if res.failed:
        return False
    res = run('mv {0}{1}/web_static/* {0}{1}/'.format(path, file_noext))
    if res.failed:
        return False
    res = run('rm -rf {}{}/web_static'.format(path, file_noext))
    if res.failed:
        return False
    res = run('rm -rf /data/web_static/current')
    if r.failed:
        return False
    res = run('ln -s {}{}/ /data/web_static/current'.format(path, file_noext))
    if res.failed:
        return False
    return True
