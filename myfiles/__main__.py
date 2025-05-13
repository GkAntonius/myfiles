import sys
from pathlib import Path

from .config import UserConfig, ProjectConfig
from .nodeproject import Project, Node

def main():
    UserConfig.new_config_file()
    print_user_config()
    #print_project()
    #print_node()

def print_user_config():
    rc = UserConfig.from_config_files()
    print(rc)

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
