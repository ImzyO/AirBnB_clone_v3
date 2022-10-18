#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the web_static folder of your AirBnB Clone repo"""

from fabric.operations import local
from datetime import datetime

def do_pack():
    """function to compress file"""
    date_time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    path = "versions/web_static_{}.tgz".format(date_time)
    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(path))
    if result.failed:
        return None
    return path
