from .. import UserConfig, ProjectConfig, RemoteHosts
from .. import Node, Project


# =========================================================================== #
# Configurating and inspecting
# =========================================================================== #

def check_config():

    userconfig = UserConfig()
    if not userconfig.file_exists:
        userconfig.write_config_file()

    try:
        projconfig = ProjectConfig()
        print(projconfig)

        if not projconfig.file_exists:
            if projconfig.topdir.exists():
                projconfig.write_config_file()
    except:
        pass

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

def newproj(name):
    return Project.new_project(name)

# =========================================================================== #
# Syncing data
# =========================================================================== #

def pull_remote(hostname, ids):
    proj = Project()
    proj.pull_production_dir(hostname, ids)

def push_remote(hostname, ids):
    proj = Project()
    proj.push_production_dir(hostname, ids)

def pull_scratch(ids):
    proj = Project()
    proj.pull_scratch(ids)

def push_scratch(ids):
    proj = Project()
    proj.push_scratch(ids)

def push_local_data(hostname):
    proj = Project()
    proj.push_local_data(hostname)

def push_glocal_data(hostname):
    proj = Project()
    proj.push_global_data(hostname)


# =========================================================================== #
# Moving data
# =========================================================================== #


def make_anadir(ids):
    node = Node(ids)
    node.make_analysis_dir(verbose=True)

def save_results():
    project = Project()
    project.copy_analysis_files_to_results()
    pass
