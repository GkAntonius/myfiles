import os
from .indices import read_ids, ids_match

__all__ = ['find_calc_dir', 'find_data_dir', 'find_data_fname', 'find_data_file', 'get_data_fname', 'get_data_file']

def find_data_fname(ids, where='.', prefix='data', sep='-', tag=None):
    ids = listify(ids)

    for fname in os.listdir(where):

        if fname.startswith(prefix):
            pruned_fname = fname.lstrip(prefix).lstrip(sep)
        else:
            continue

        fname_ids = read_ids(pruned_fname)
        if ids_match(ids, fname_ids):
            if tag and tag not in fname:
                continue
            return os.path.join(where, fname)

    raise Exception(
        'Did not find any file matching ids {} in directory {}'.format(
        ids, where))

# Cant seem to decide on a name...
get_data_fname = find_data_fname
find_data_file = find_data_fname
get_data_file = find_data_fname

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
                topdir = os.path.join(topdir, subdir)
                found += 1
                break

    if found < len(ids):

        raise Exception('Could not find calculation directory.\n' +
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
