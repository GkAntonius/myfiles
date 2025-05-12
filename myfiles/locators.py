import os
from .indices import (
    read_ids, read_path_ids, ids_match, trim_ids,
    ids_startswith, ids_tail_match_head, ids_match_tail,
    )

__all__ = [
    'find_calc_dir', 'find_data_dir', 'find_data_fname',
    'find_data_file', 'get_data_fname', 'get_data_file',
    'find_data_subdir',
    ]

def iter_subdir(topdir):
    for subdir in os.listdir(topdir):
        if os.path.isdir(os.path.join(topdir, subdir)):
            yield subdir


def find_data_fname(ids, where='.', sep='-', prefix=None, tag=None,
                    ext=None,
                    recursive=True,
                    ids_include_directory=False,
                    accumulate_ids=True,
                    data_dir=True,
                    ):
    """
    Search for a file with specific ids, within a certain directory.
    Raise an exception if file is not found.

    Examples:

        >>> find_data_file([116, 400], where='116-xct-ph-test/Data/')
        '116-xct-ph-test/Data/data-116-400-xctph.nc'

        >>> find_data_file([116, 400, 3], where='116-xct-ph-test/Data',
                           ids_include_directory=True, accumulate_ids=True)
        '116-xct-ph-test/Data/116-400-bse-qgrid/data-3-bse.nc'

        >>> find_data_file([116, 116, 400], where='116-xct-ph-test/Data/',
                           ids_include_directory=True, accumulate_ids=True)
        '116-xct-ph-test/Data/data-116-400-xctph.nc'

        >>> find_data_file([3], where='116-xct-ph-test/Data',
        '116-xct-ph-test/Data/116-400-bse-qgrid/data-3-bse.nc'


    """
    ids = listify(ids)

    # Scan all the files in the directory
    for fname in os.listdir(where):
        fname_fullpath = os.path.join(where, fname)

        if os.path.isdir(fname_fullpath) and not data_dir:
            continue

        if tag and tag not in fname:
            continue

        if prefix and not fname.startswith(prefix):
            continue

        if ext is not None:
            if not fname.endswith(ext):
                continue

        fname_scan = fname.lstrip(prefix).lstrip(sep)

        if ids_include_directory:
            fname_scan = os.path.join(where, fname_scan)
            
        fname_ids = read_path_ids(fname_scan)

        if ids_match(ids, fname_ids):
            return fname_fullpath

    # Descend into each subdirectory and look for files
    if recursive:

        kwargs = dict(recursive=recursive, sep=sep, prefix=prefix, tag=tag,
                      ids_include_directory=ids_include_directory,
                      accumulate_ids=accumulate_ids)

        for subdir in iter_subdir(where):
            subdir_fullpath = os.path.join(where, subdir)


            if accumulate_ids:
                subdir_ids = read_ids(subdir)
                if not ids_startswith(ids, subdir_ids):
                    continue

                kwargs['ids'] = trim_ids(ids, subdir_ids)
            else:
                kwargs['ids'] = ids

            try:
                return find_data_fname(where=subdir_fullpath, **kwargs)
            except:
                pass

    raise Exception(
        'Did not find any file matching ids {} in directory {}'.format(
                                                                    ids, where)
        )


# GKA: Cant seem to decide on a name...
get_data_fname = find_data_fname
find_data_file = find_data_fname
get_data_file = find_data_fname



def find_data_subdir(ids, where='.'):
    """
    Scan recursively a directory to find one directory whose sequence
    matches ids. 
    """
    
    for subdir in iter_subdir(where):
        subdir_fullpath = os.path.join(where, subdir)

        subdir_ids = read_ids(subdir)
        subdir_path_ids = read_path_ids(subdir_fullpath)

        if ids_match(ids, subdir_ids) or ids_match_tail(ids, subdir_path_ids):
            return subdir_fullpath

        elif ids_tail_match_head(subdir_path_ids, ids):
            try:
                return find_data_subdir(ids, where=subdir_fullpath)
            except:
                pass

    raise Exception('could not find calculation directory.\n' +
        'directory: {}\n'.format(where) +
        'ids: {}\n'.format(ids)
        )



def find_calc_dir(ids, where=None):
    """
    Find a calculation directory inside the production directory (where)
    for which each subdirectory is identified with one element of ids.
    The subdirectory depth matches the length of ids.
    """
    ids = listify(ids)

    if not where:
        from .filebuttler import production_dir
        where = production_dir

    found = 0
    topdir = where
    for idi in ids:
        for subdir in os.listdir(topdir):
            idsub = read_ids(subdir)
            if idsub and idi == idsub[0]:
                path = os.path.join(topdir, subdir)
                if not os.path.isdir(path):
                    continue
                topdir = path
                found += 1
                break

    if found < len(ids):

        raise Exception('could not find calculation directory.\n' +
            'directory: {}\n'.format(where) +
            'ids: {}\n'.format(ids)
            )

    return topdir


def find_data_dir(ids, where=None, data_subdir_name='Data'):
    """
    Find a Data directory inside a calculation directory (identified with ids)
    inside the production directory (where)
    for which each subdirectory is identified with one element of ids.
    The subdirectory depth matches the length of ids.
    """
    ids = listify(ids)
    calc_dir = find_calc_dir(ids, where=where)
    if not data_subdir_name:
        return calc_dir
    data_dir = os.path.join(calc_dir, data_subdir_name)
    if not os.path.exists(data_dir):
        raise Exception(
            'Could not find data directory within calculation directory:\n'
            + calc_dir)
    return data_dir


def listify(obj):
    try:
        return list(obj)
    except:
        return [obj]
