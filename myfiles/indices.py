import os
from copy import copy

import __main__ as main
#print(main.__file__)

__all__ = ['get_ids', 'read_ids', 'ids_match']

home = os.path.realpath(os.environ['HOME'])

try:
    _main_default_fname = main.__file__
except:
    _main_default_fname = ''

def get_ids(fname=_main_default_fname, n=None, rev=False):
    """
    Generate id numbers from the full path of the current file.
    For example, a full file path
    Example:
        > get_ids('/path/to/the/file/1-calculation/002-sub-calc/file-50.py', n=2)
        > [2, 50]

    Arguments
    ---------
    n: Number of indices to be returned. Defaults to all indices.
    rev: If True, return the indicies extracted from right to left.
    """

    if n is None:
        nmax = float('inf')
    else:
        nmax = n

    fullpath = os.path.realpath(fname)
    fullpath = fullpath.split(home)[-1]

    ids = list()

    rest = copy(fullpath)
    i = 0
    while True:
        #i += 1
        #rest,  last = os.path.split(rest)
        #this_id = starting_or_ending_digit(last)
        rest,  last = os.path.split(rest)
        these_ids = read_ids(last)
        ids.extend(reversed(these_ids))
        #if len(ids) >= nmax:
        #    ids = ids[:nmax]
        #    break
        if not rest or not last:
            break
        #if this_id == 0:
        #    break

        #ids.append(this_id)

    nids = len(ids)

    if not nids:
        raise Exception('Could not extract ids from file name:\n\t{}'.format(fullpath))

    if n and nids < n:
        import warnings
        warnings.warn('Found less than {} ids in file name:\n\t{}'.format(fullpath))

    if not rev:
        ids = list(reversed(ids))

    if n is not None:
        ids = ids[:n]

    return ids



def starting_or_ending_digit(basename, sep='-'):
    """Extract the digits at the start or the end of a name."""
    tokens = os.path.splitext(basename)[0].split(sep)
    if tokens[0].isdigit():
        return int(tokens[0])
    elif tokens[-1].isdigit():
        return int(tokens[-1])
    else:
        return 0


def read_ids(fname, sep='-'):
    """Read the ids from a file basename."""
    basename = os.path.splitext(fname)[0]
    ids = list()
    for tok in basename.split(sep):
        if tok.isdigit():
            ids.append(int(tok))
    return ids


def ids_match(ids1, ids2):
    if len(ids1) != len(ids2):
        return False
    for i, j in zip(ids1, ids2):
        if i != j:
            return False
    return True
             

