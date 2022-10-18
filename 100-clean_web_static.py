#!/usr/bin/python3
"""distributes an archive to your web servers, using the function do_deploy:"""
from os.path import exists
from datetime import datetime
from fabric.api import local, env, put, run

env.hosts = ['3.229.120.108', '44.192.24.108']

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
    
def deploy():
    """Creates and distributes an archive to a web server"""
    filepath = do_pack()
    if filepath is None:
        return False
    d = do_deploy(filepath)
    return d 
    
    def do_clean(number=0):
    """Deletes out-of-date archives"""
    files = local("ls -1t versions", capture=True)
    file_names = files.split("\n")
    n = int(number)
    if n in (0, 1):
        n = 1
    for i in file_names[n:]:
        local("rm versions/{}".format(i))
    dir_server = run("ls -1t /data/web_static/releases")
    dir_server_names = dir_server.split("\n")
    for i in dir_server_names[n:]:
        if i is 'test':
            continue
        run("rm -rf /data/web_static/releases/{}".format(i))
