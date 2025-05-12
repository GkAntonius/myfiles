import sys

from .config import UserConfig
from .nodeproject import Project, Node

def main():
    print_user_config()
    print_project()
    #print_node()

def print_user_config():
    rc = UserConfig.from_config_file()
    print(rc)

def print_project():
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
