import os
from copy import copy

import __main__ as main

__all__ = [
    'get_ids', 'read_ids', 'read_path_ids', 'ids_match',
    'get_tag', 'read_tag', 'trim_ids', 'ids_startswith',
    'ids_tail_match_head', 'ids_match_tail',
    ]

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

    fullpath = os.path.realpath(fname)
    fullpath = fullpath.split(home)[-1]

    ids = read_path_ids(fullpath)

    nids = len(ids)

    if not nids:
        raise Exception('Could not extract ids from file name:\n\t{}'.format(fullpath))

    if n and nids < n:
        import warnings
        warnings.warn('Found less than {} ids in file name:\n\t{}'.format(fullpath))

    if n is not None:
        ids = ids[-n:]

    if rev:
        ids = list(reversed(ids))

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

def read_path_ids(fname, sep='-'):
    """
    Read the ids from a file path, (absolute or not).
    Extend the indices with each directory.
    """
    ids = list()
    rest = fname
    while rest and rest != '/':
        rest, last = os.path.split(rest)
        ids_p = read_ids(last, sep=sep)
        ids.extend(reversed(ids_p))
    return list(reversed(ids))


def ids_match(ids1, ids2):
    if len(ids1) != len(ids2):
        return False
    for i, j in zip(ids1, ids2):
        if i != j:
            return False
    return True

def ids_tail_match_head(scantail, scanhead):
    """Does the ending sequence of 'scantail' match the start of 'scanhead' """
    n = len(scanhead)
    m = len(scantail)
    for i in range(1, min(m,n)):
        if ids_match(scantail[-i:], scanhead[:i]):
            return True
    return False

def ids_match_tail(ids, scantail):
    """Does the ending sequence of 'scantail' match the start of 'scanhead' """
    n = len(ids)
    m = len(scantail)
    if m < n:
        return False
    return ids_match(ids, scantail[-n:])

def ids_startswith(ids, start):
    if len(start) > len(ids):
        return False
    ids = list(ids)
    for i in start:
        j = ids.pop(0)
        if i != j:
            return False
    return True



def get_tag(fname=_main_default_fname):
    fullpath = os.path.realpath(fname)
    fullpath = fullpath.split(home)[-1]
    rest,  last = os.path.split(fullpath)
    tag = read_tag(last)
    return tag



def read_tag(fname, sep='-'):
    """
    Strip numbers ids out of a file name to return literal part.
    Example:

        read_tag('plot-100-20-spectral-function.py')
        >>> 'spectral-function'
    """
    basename = os.path.splitext(fname)[0]
    words = []
    phrases = []

    # Here we allow for one sequence of indices to appear
    # in the middle of the file name
    for tok in basename.split(sep):
        if tok.isdigit():
            if not phrases:
                phrases.append([])
            elif phrases[-1]:
                phrases.append([])
        else:
            words.append(tok)
            if not phrases:
                phrases.append([])
            words.append(tok)
            phrases[-1].append(tok)

    # No, we still want to scan a single phrase
    #if len(phrases) < 2:
    #    return sep.join(phrases[0])

    # Checke the first word and try to classify file
    known_prefix = ('plot', 'data', 'run', 'flow',)
    if phrases[0][0] in known_prefix:
        del phrases[0][0]

    if phrases:
        if not phrases[0]:
            del phrases[0]

    # Now construct the tag
    if len(phrases) < 2:
        return sep.join(phrases[0])

    # Just concatenate everything
    return sep.join([sep.join(p) for p in phrases])


def trim_ids(ids, clip):
    """
    Pop the parents_ids from the start of ids.
    trim([1,2,3], [1,2])
    >>> [3]
    """
    trimmed_ids = list(ids)
    for i in clip:
        if i == trimmed_ids[0]:
            trimmed_ids.pop(0)
        else:
            break
    return trimmed_ids
