from .data import DataDirs
from .config import UserConfig, ProjectConfig
from .nodeproject import Project, Node, NodeID
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

def get_structure_dir():
    return DataDirs().get_structure_dir()

def get_structure(filename):
    """Return absolute paths of a structure"""
    return DataDirs().get_structure(filename)

def get_pseudo(psps, subdir=None):
    """Return list of absolute psp paths"""
    return DataDirs().get_pseudo(psps, subdir=subdir)

def get_pseudo_dir(subdir=None):
    return DataDirs().get_pseudo_dir(subdir=subdir)

def find_calc_dir(psps):
    """Find a calculation directory using full path info."""
    pass
