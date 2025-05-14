import sys
from pathlib import Path

from .config import UserConfig, ProjectConfig
from .nodeproject import Project, Node

def main():
    check_user_config()
    check_project_config()
    check_project()
    check_node()


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

def check_node():
    node = Node()
    if node:
        node.scan()
        print(node)

if __name__ == "__main__":
    sys.exit(main())
