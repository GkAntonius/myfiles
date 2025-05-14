from pathlib import Path
from .config import UserConfig, ProjectConfig, NodeConfig
from .nodeid import NodeID

__all__ = ['Project', 'Node']

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


class Node:
    """
    A node represents a calculation that we perform and analyse,
    which is identified by a NodeID and a name.
    Several directories may share the node information, in particular:
    - A production directory
    - An analysis directory
    """
    def __init__(self, ids=None, config=None):

        self.config = config or NodeConfig()
        self.name = self.config['Node']['name']

        if ids is None:
            self.ids = NodeID.from_path()
        else:
            self.ids = NodeID(ids)

        self.project = Project()

        # Sub nodes
        self.nodes = []

        # Files and directories
        self.production_files = []
        self.production_directories = []

        self.analysis_files = []
        self.analysis_directories = []

        self.results_directories = []
        self.results_files = []

        #if not self.ids:
        #    raise Exception('Node has no id.')

    def __bool__(self):
        return bool(self.ids)

    @classmethod
    def from_path(cls, path='.', **kwargs):
        ids = NodeId.from_path(path)
        cls(ids, **kwargs)

    def __str__(self):
        S = ''
        header = f'Node {self.ids}'
        n = 4 * len(header)
        S += n*'=' + '\n'
        S += header + '\n'
        S += n*'-' + '\n'
        S += 'Configuration files: \n'
        for fname in self.config.files_read:
            S += str(Path(fname).absolute()) + '\n'
        S += n*'-' + '\n'
        S += f'Production directories and files:\n'
        for p in self.production_directories + self.production_files:
            S += f'    {p}\n'
        S += n*'-' + '\n'
        S += f'Analysis directories and files:\n'
        for p in self.analysis_directories + self.analysis_files:
            S += f'    {p}\n'
        S += n*'-' + '\n'
        S += f'Results directories and files:\n'
        for p in self.results_directories + self.results_files:
            S += f'    {p}\n'
        S += n*'=' + '\n'
        return S


    def scan(self):
        """
        Find all files and directories belonging to this node.
        Those files must have arbitrary names, but their id
        structure must match those of the node or its subnodes.
        """
        self.scan_production()
        self.scan_analysis()
        self.scan_results()

    def scan_production(self):
        """
        Look for matching files and directories in project's production dir.
        """
        self.production_directories, self.production_files = (
            self.ids.scan_directory(self.project.production)
            )

    def scan_analysis(self):
        """
        Look for matching files and directories in project's analysis dir.
        """
        self.analysis_directories, self.analysis_files = (
            self.ids.scan_directory(self.project.analysis)
            )

    def scan_results(self):
        """
        Look for matching files and directories in project's analysis dir.
        """
        self.results_directories, self.results_files = (
            self.ids.scan_directory(self.project.results)
            )

    @property
    def basename(self):
        base, rest = self.ids.partition(1)
        return str(base) + '-' + self.name

    @property
    def production(self):
        return self.project.production / self.basename

    @property
    def analysis(self):
        return self.project.analysis / self.basename

    def find_production_dir(self, ids=None):
        """
        Search for a production directory in node that matches exactly
        some ids or the node's ids.
        """ 
        if ids is None:
            ids = self.ids
        else:
            ids = NodeID(ids)

        if not self.production_directories:
            self.scan_production()

        found = []
        for path in self.production_directories:
            pathID = NodeID.from_path(path)

            if pathID == ids:
                found.append(str(path))

        if not found:
            S = f'Did not find any production directory matching: {ids}\n'
            S += f'Project production directory: {self.project.production}\n'
            S += f'Node production directory: {self.production_directories}\n'
            raise Exception(S)

        return found[0]

    def make_filename(self, basename, ext):
        return str(self.ids) + '-' + basename

    def new_filename(self, name, where='.', ext=''):
        """
        Generate a filename in a specified directory.
        """
        pass

    #def find_subdir(self, where):
    #    """
    #    Use own ids, and possibly name to search for a subdirectory directory
    #    belonging to this node.
    #    """ 
    #    pass

