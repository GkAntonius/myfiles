from abc import abstractmethod, ABC
from argparse import ArgumentParser, Namespace


def get_cli_functions():
    """Return a list of callable functions."""
    functions = []
    for fclass in _get_all_subclasses(CLIfunction):
        try:
            func = fclass()
            name = fclass.__name__
            functions.append((name, func))
        except TypeError:
            continue
    functions = sorted(functions, key=lambda f: f[0])
    names, funcs = zip(*functions)
    return funcs

def _get_all_subclasses(cls):
    """Recursively retrieve all subclasses of a given class."""
    all_subclasses = set()
    for subclass in cls.__subclasses__():
        all_subclasses.add(subclass)
        all_subclasses.update(_get_all_subclasses(subclass))
    return list(all_subclasses)

# =========================================================================== #
# Base classes
# =========================================================================== #

class CLIfunction(ABC):
    """Base class for functions with command-line interface."""

    @abstractmethod
    def __call__(self, args: Namespace):
        pass

    def add_parser(self, subparsers) -> ArgumentParser:
        parser = subparsers.add_parser(self.__class__.__name__,
                                       help=self.__class__.__doc__)
        parser.set_defaults(func=self)
        return parser


class CLIfunctionWithID(CLIfunction):
    """Base class for functions that operate on a node ID."""

    def add_parser(self, sub):
        parser = super().add_parser(sub)
        parser.add_argument('ids', type=int, nargs='+', help='Node ID.')
        return parser


class CLIfunctionWithRemote(CLIfunction):
    """Base class for functions that operate on a remote host."""

    def add_parser(self, sub):
        parser = super().add_parser(sub)
        parser.add_argument('hostname', type=str, help='Remote host.')
        return parser

# =========================================================================== #
# Functions
# =========================================================================== #

from .. import UserConfig, ProjectConfig, RemoteHosts
from .. import Node, Project

# =========================================================================== #

class check_config(CLIfunction):
    """Print out configuration."""
    def __call__(self, args):

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

class check_remote(CLIfunction):
    """Print out remote hosts."""
    def __call__(self, args):
        rh = RemoteHosts()
        print(rh)

class check_project(CLIfunction):
    """Display project information."""
    def __call__(self, args):
        proj = Project()
        print(proj)
    
class check_user_config(CLIfunction):
    """Print out user configuration."""
    def __call__(self, args):
        rc = UserConfig()
        print(rc)
        if not rc.file_exists:
            rc.write_config_file()

class check_project_config(CLIfunction):
    """Print out project configuration."""
    def __call__(self, args):
        rc = ProjectConfig()
        print(rc)
        if not rc.file_exists:
            rc.write_config_file()

class check_node(CLIfunctionWithID):
    """Print out information about a node."""

    def __call__(self, args):
        node = Node(ids=args.ids)
        if node:
            node.scan()
            print(node)
        else:
            print(node.ids)

class newproj(CLIfunction):
    """
    Create a new project, with directories and configuration files.
    Will not overwrite an existing project.
    """
    def add_parser(self, sub):
        parser = super().add_parser(sub)
        parser.add_argument('name', type=str, help='Project name')
        return parser

    def __call__(self, args):
        return Project.new_project(args.name)

# =========================================================================== #

class pull_remote(CLIfunctionWithRemote, CLIfunctionWithID):
    """Pull files from a remote host."""
    def __call__(self, args):
        proj = Project()
        proj.pull_production_dir(args.hostname, args.ids)

class push_remote(CLIfunctionWithRemote, CLIfunctionWithID):
    """Push files to a remote host."""
    def __call__(self, args):
        proj = Project()
        proj.push_production_dir(args.hostname, args.ids)

class pull_scratch(CLIfunctionWithID):
    """Pull files from scratch directory."""
    def __call__(self, args):
        proj = Project()
        proj.pull_scratch(args.ids)

class push_scratch(CLIfunctionWithID):
    """Push files to scratch directory."""
    def __call__(self, args):
        proj = Project()
        proj.push_scratch(args.ids)

class push_local_data(CLIfunctionWithRemote):
    """Push local data to a remote host."""
    def __call__(self, args):
        proj = Project()
        proj.push_production_dir(args.hostname, args.ids)
        proj.push_local_data(args.hostname)

class push_global_data(CLIfunctionWithRemote):
    """Push global data to a remote host."""
    def __call__(self, args):
        proj = Project()
        proj.push_global_data(args.hostname)

# =========================================================================== #
# Moving data
# =========================================================================== #

class make_anadir(CLIfunctionWithID):
    """Create a directory in analysis folder to match one in the production folder."""
    def __call__(self, args):
        node = Node(ids)
        node.make_analysis_dir(verbose=True)


class save_results(CLIfunction):
    """Create a directory in analysis folder to match one in the production folder."""
    def __call__(self, args):
        project = Project()
        project.copy_analysis_files_to_results()
