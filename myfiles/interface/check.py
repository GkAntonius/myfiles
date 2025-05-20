from .. import UserConfig, ProjectConfig, RemoteHosts
from .. import Node, Project

def check_config():

    userconfig = UserConfig()
    if not userconfig.file_exists:
        userconfig.write_config_file()

    projconfig = ProjectConfig()
    print(projconfig)

    if not projconfig.file_exists:
        if projconfig.topdir.exists():
            projconfig.write_config_file()

    rh = RemoteHosts()
    print(rh)


def check_user_config():
    rc = UserConfig()
    print(rc)
    if not rc.file_exists:
        rc.write_config_file()

def check_project_config():
    rc = ProjectConfig()
    print(rc)
    if not rc.file_exists:
        rc.write_config_file()

def check_remote():
    rh = RemoteHosts()
    print(rh)

def check_node(ids=None):
    node = Node(ids=ids)
    if node:
        node.scan()
        print(node)
    else:
        print(node.ids)

def check_project():
    proj = Project()
    print(proj)
