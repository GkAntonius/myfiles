from pathlib import Path
import shutil
from .config import UserConfig, ProjectConfig, NodeConfig, RemoteHosts
from .nodeid import NodeID
from .util import prompt_user_and_run
import subprocess

__all__ = ['Node']

class Node:
    """
    A node represents a calculation that we perform and analyse,
    which is identified by a NodeID and a name.
    Several directories may share the node information, in particular:
    - A production directory
    - An analysis directory
    """
    def __init__(self, ids=None, config=None, project=None):

        if config is None:
            self.config = NodeConfig()
        else:
            self.config = config

        self.name = self.config['Node']['name']

        if ids is None:
            self.ids = NodeID.from_path()
        else:
            self.ids = NodeID(ids)

        if project is None:
            from .project import Project
            self.project = Project()
        else:
            self.project = project

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

    _name = NodeConfig.node_defaults['Node']['name']
    @property
    def name(self):
        if self._name == NodeConfig.node_defaults['Node']['name']:
            self.find_name()
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @classmethod
    def from_path(cls, path='.', **kwargs):
        ids = NodeID.from_path(path)
        return cls(ids, **kwargs)

    @property
    def basename(self):
        name = self.name  # First find the name, if undefined,
                          # which can modify ids format.
        return self.ids.trim(1).tag + name

    # GA: Not sure about this. The name in analysis doesnt need to match
    #     the name in production...

    @property
    def production(self):
        return self.project.production / self.basename

    @property
    def analysis(self):
        return self.project.analysis / self.basename

    def __bool__(self):
        return bool(self.ids)

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
        Look for matching files and directories in project's results dir.
        """
        self.results_directories, self.results_files = (
            self.ids.scan_directory(self.project.results)
            )

    def copy_analysis_files_to_results(self, exclude=('.py',), verbose=True):
        """
        Look for files produced in analysis directory and copy them to
        the results directory.
        """
        if isinstance(exclude, str):
            exclude = [exclude]
        files_to_copy = []
        # ---------------------
        # GA: Temporarily backtracking to python 3.11 compatible version.
        #for (dirpath, dirnames, filenames) in self.analysis.walk():
        for root, dirnames, filenames in os.walk(str(self.analysis)):
            dirpath = Path(root)
        # ---------------------

            for filename in filenames:
                skip = False
                for ext in exclude:
                    if filename.endswith(ext):
                        skip = True
                        break
                if skip:
                    continue

                files_to_copy.append(dirpath / filename)

        for filename in files_to_copy:
            ids = NodeID.from_path(filename)
            name = ids.strip_ids(filename)
            results_filename = ids.make_filename(name)
            source = filename
            target = self.project.results / results_filename
            if not target.exists():
                print(f'Copying: {source} --> {target}')
                shutil.copy(source, target)

        return


    def find_production_dir(self):
        """
        Search for a production directory in node that matches exactly
        some ids or the node's ids.
        """ 
        if not self.production_directories:
            self.scan_production()

        found = []
        for path in self.production_directories:
            pathID = NodeID.from_path(path)

            if pathID == self.ids:
                found.append(str(path))

        if not found:
            S = f'Did not find any production directory matching: {ids}\n'
            S += f'Project production directory: {self.project.production}\n'
            S += f'Node production directory: {self.production_directories}\n'
            raise Exception(S)

        return found[0]

    def find_name(self):
        """
        Find the name of the node by looking for a production directory
        that matches the ids.
        Side effect: read the ids from the production directory
        """
        production_dir = self.find_production_dir()
        basename = Path(production_dir).name
        self.name = self.ids.strip_ids(basename)
        self.ids = self.ids.from_path(production_dir)
        return self.name

    def make_analysis_dir(self, verbose=True):
        if verbose:
            print(self.analysis)
        self.analysis.mkdir(exist_ok=True)

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

