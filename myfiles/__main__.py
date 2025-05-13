import sys
from pathlib import Path

from .config import UserConfig, ProjectConfig, CONFIG_FILENAME
from .nodeproject import Project, Node

def main():
    write_user_config()
    print_user_config()
    #print_project()
    #print_node()

def print_user_config():
    rc = UserConfig.from_config_files()
    print(rc)

def write_user_config():
    target = Path('~').expanduser().absolute() / CONFIG_FILENAME
    if not target.exists():
        answer = input(f"File '~/{CONFIG_FILENAME}' does not exist. \n"
                       "Do you want to write a new one? [y/N]: ")

        if answer.lower().startswith('y'):
            rc = UserConfig.from_config_files([])
            rc.write(str(target))
            print(f"Wrote file '~/{CONFIG_FILENAME}'.")
    #else:
    #    print("Cannot overwrite existing file '~/.myfilesrc'.")

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
