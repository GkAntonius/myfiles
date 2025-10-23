from pathlib import Path
from argparse import ArgumentParser
from textwrap import dedent

from ..config import UserConfig, ProjectConfig
from ..nodeid import NodeID
from ..node import Node
from ..project import Project
from ..util import ScanResult
from ..data import DataDirs

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

def get_structure_file(filename):
    """Return absolute paths of a structure."""
    return DataDirs().get_structure_file(filename)

get_structure = get_structure_file

def get_pseudo_dir(subdir=None, keywords=()):
    """Return absolute paths of a pseudopotential directory."""
    return DataDirs().get_pseudo_dir(subdir=subdir, keywords=keywords)

def get_pseudopotentials(*args, **kwargs):
    """
    Return list of absolute psp paths.
    """
    return DataDirs().get_pseudopotentials(*args, **kwargs)

get_pseudos = get_pseudopotentials
get_pseudo = get_pseudopotentials

def get_production_dir(ids=None):
    """Find a production directory matching some ids."""
    node = Node(ids=ids)
    return node.find_production_dir()

find_production_dir = get_production_dir
find_calc_dir = get_production_dir

def get_workdir(name, ids=None):
    if ids is None:
        pids = NodeID.from_parent_path()
        ids = NodeID.from_path()
        if m := len(pids) < len(ids):
            _, ids = ids.partition(m)
            ids.ndigits = 1
    else:
        ids = NodeID(ids)

    return Path(f'{ids}{ids.sep}{name}')

def get_filename(name, ids=None, ext='', where='.', sep='-'):
    if ids is None:
        pids = NodeID.from_parent_path()
        ids = NodeID.from_path()
        if m := len(pids) < len(ids):
            _, ids = ids.partition(m)
    else:
        ids = NodeID(ids)

    basename = str(name)
    if ext:
        basename += '.' + ext.lstrip('.')

    filename = f'{ids}{ids.sep}{basename}'
    return Path(where) / filename

make_filename = get_filename

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


def get_datafile(filename):
    data = DataDirs()
    result, datafile = data.get_datafile(filename)
    if result == ScanResult.success:
        return datafile
    elif result == ScanResult.no_scan:
        raise Exception('No data directory to scan.')
    else:
        raise Exception(f'File not found: {filename}')
