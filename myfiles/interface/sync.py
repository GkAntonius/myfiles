from .. import UserConfig, ProjectConfig, RemoteHosts
from .. import Node, Project

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
