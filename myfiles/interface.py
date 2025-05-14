"""
Interface functions
"""
from pathlib import Path
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


# GA: Not sure I will keep the following.

def make_data_fname(ids, where='.', tag='', ext='.dat', prefix='data',
                    sep='-', rel=True, create=True):
    """
    Example:
        > make_data_fname([1,2,3], where='Data', tag='example')
        > 'Data/data-1-2-3-example.dat'
    """

    tokens = list()

    if prefix:
        tokens.append(prefix) 

    if ids:
        tokens.extend(ids)

    if tag:
        tokens.append(tag.replace(' ', sep))

    data_fname = sep.join(map(str, tokens))

    if ext:
        data_fname += '.' + ext.lstrip('.')

    path = Path(where)

    if create:
        path.mkdir(exist_ok=True)

    return str(path / data_fname)


def make_plot_fname(ids, where='.', tag='', ext='.pdf', prefix='plot',
                    **kwargs):
    """
    Example:
        > make_plot_fname([1,2,3], where='Plots', tag='example')
        > 'Plot/data-1-2-3-example.dat'
    """
    return make_data_fname(ids, where, tag, ext, prefix, **kwargs)

