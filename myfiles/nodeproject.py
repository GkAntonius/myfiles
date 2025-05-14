from pathlib import Path
from .config import UserConfig, ProjectConfig

__all__ = ['Project', 'Node', 'NodeID']

class Project:

    def __init__(self, config=None, path='.'):
        config = config or ProjectConfig(path=path)
        self.config = config
        self.name = str(config['Project']['name'])
        self.topdir = config.topdir
        self.local_data = self.topdir / config['Local']['data']
        self.production = self.topdir / config['Local']['production']
        self.analysis = self.topdir / config['Local']['analysis']
        self.results = self.topdir / config['Local']['results']

    def __str__(self):
        S = ''
        header = f'Project {self.name}'
        n = 2 * len(header)
        S += n*'=' + '\n'
        S += header + '\n'
        S += f'Top directory: {self.topdir}\n'
        S += n*'-' + '\n'
        S += 'Configuration files: \n'
        for fname in self.config.files_read:
            S += str(Path(fname).absolute()) + '\n'
        S += n*'-' + '\n'
        S += f'Directories:\n'
        for p in (self.local_data,self.production,
                  self.analysis,self.results):
            S += f'    {p}\n'
        S += n*'=' + '\n'
        return S

    #@classmethod
    #def from_path(cls, workdir=None):
    #    """
    #    Scan a path and try to figure out the top directory
    #    for this project.
    #    """
    #    if workdir is None:
    #        workdir = Path('.')
    #    else:
    #        workdir = Path(workdir)

    #    workdir = workdir.expanduser().resolve()
    #    userconfig = UserConfig.from_config_files()
    #    projectsdir = userconfig.projectsdir

    #    if workdir == projects:
    #        raise Exception(
    #            f'Projects must be in a subdirectory of {projects}')

    #    # GA: Will not work if executed from a scratch directory
    #    #     The solution is to have a project config file telling us
    #    #     the project topdir.
    #    for p in workdir.parents:
    #        if p.resolve() == projectsdir:
    #            break
    #    else:
    #        raise Exception(
    #            f'Projects must be in a subdirectory of {projects}')

    #    p = workdir.relative_to(projects)
    #    topdir = projects / p.parts[0]

    def from_node(cls, node):
        pass

    def new_node(self, ids, name):
        pass

    def iter_nodes(self):
        pass

    def view(self):
        """Find directories and nodes, and print out information."""
        pass

    def create_anadir(self):
        pass

    def sync_plots(self):
        pass

    def pull_production_dir(self, remotehost, remote_project_dir, ids):
        pass

    def pull_analysis_dir(self, remotehost, remote_project_dir, ids):
        pass


class NodeID(list):
    """A sequence of digits identifying a node."""
    sep = '-'

    def __init__(self, ids: [int]):
        super().__init__(ids)

    def extend(self, ids:[int]):
        super().extend(list(ids))

    @classmethod
    def from_path(cls, path: str, n='*'):
        path = str(path)

    def from_basename(cls, fname: str, n='*'):
        """Read the ids from a file basename."""
        fname = str(fname)
        ids = list()
        for tok in fname.split(self.sep):
            if tok.isdigit():
                ids.append(int(tok))
        return cls(ids)

    def is_empty(self):
        """A node is empty if all its directories are empty."""
        return False

    def __str__(self):
        return self.sep.join(str(i) for i in self.ids)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i, j in zip(self, other):
            if i != j:
                return False
        return True


class Node:
    """
    A node represents a calculation that we perform and analyse,
    which is identified by a NodeID and a name.
    Several directories may share the node information, in particular:
    - A production directory
    - An analysis directory
    """
    
    def __init__(self, ids: [int], n=None, name=''):
        self.id = NodeID(ids)
        self.name = name
        self.project = None

    def from_filename(cls, fname=None, n='*'):
        """
        Initialize a new instance from the current filename,
        or one specified explicitly. 
        """
        pass

    @classmethod
    def from_path(cls, path: str | Path):
        pass

    def new_filename(self, name, where='.', ext=''):
        """
        Generate a filename in a specified directory.
        """
        pass

    def find_subdir(self, where):
        """
        Use own ids, and possibly name to search for a subdirectory directory
        belonging to this node.
        """ 
        pass

    #def find_production_dir(self):
    #    """
    #    Use own ids, and possibly name to search for a production directory.
    #    """ 
    #    return self.find_subdir()
