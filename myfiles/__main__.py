import sys
from pathlib import Path

from .config import UserConfig, ProjectConfig
from .nodeproject import Project, Node

def main():
    check_user_config()
    check_project_config()
    check_project()
    #print_node()


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

def check_project():
    proj = Project()
    print(proj)

#def print_user_config():
#    rc = UserConfig.from_config_files()
#    print(rc)

def print_project():
    curdir = Path('.')
    proj = Project.from_path(curdir)
    try:
        proj = Project.from_path(__file__)
        print(proj)
    except:
        pass

def print_node():
    node = Node.from_path(__file__)
    print(node)

if __name__ == "__main__":
    sys.exit(main())
