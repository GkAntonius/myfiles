
from pathlib import Path

from .config import UserConfig, ProjectConfig

__all__ = ['Project', 'Node', 'NodeID']

class Project:
    path = '~/Projects/Someproject'
    scratch_path = 'Scratch'
    production_path = 'Production'
    analysis_path = 'Analysis'
    plots_path = 'Plots'
    data_path = 'Data'

    def __init__(self, name, workdir):
        self.name = name
        self.workdir = workdir

    @classmethod
    def from_path(cls, workdir=None):
        """
        Scan a path and try to figure out the top directory
        for this project.
        """
        pass

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
    Several directories may share the node information:
    - A production directory
    - An analysis directory
    - An plot directory
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

    def from_path(cls, pathfname: str | Path, n='*'):
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

# =========================================================================== #
# Interface funtions
# =========================================================================== #

def find_node(n='*'):
    pass

def new_workdir(name, n=1):
    """
    Scan the baseame for ids, and create a new directory full name.
    """
    pass

def get_pseudo_dir(dirname=None):
    pass

def get_structure_dir():
    pass

def find_structure(fname):
    """Return absolute paths of a structure"""
    pass

def get_pseudos(psps):
    """Return list of absolute psp paths"""
    pass

def find_calc_dir(psps):
    """Find a calculation directory using full path info."""
    pass
