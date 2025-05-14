"""
Interface functions
"""
from .data import DataDirs
from .nodeproject import Project, Node, NodeID

def get_ids(fname=None, n=None):
    """Scan the current file or path name and return ids."""
    ids = NodeID.from_path(fname)
    if n is None:
        return ids
    else:
        return ids.trim(n)

def get_structure_dir():
    """Return absolute paths of a structure directory."""
    return DataDirs().get_structure_dir()

def get_structure(filename):
    """Return absolute paths of a structure."""
    return DataDirs().get_structure(filename)

def get_pseudo(psps, subdir=None):
    """Return list of absolute psp paths."""
    return DataDirs().get_pseudo(psps, subdir=subdir)

def get_pseudo_dir(subdir=None):
    """Return absolute paths of a pseudopotential directory."""
    return DataDirs().get_pseudo_dir(subdir=subdir)

def find_production_dir(ids=None):
    """Find a production directory matching some ids."""
    node = Node(ids=ids)
    return node.find_production_dir(ids)

find_calc_dir = find_production_dir
