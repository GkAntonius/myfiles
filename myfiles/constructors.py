import os
from .indices import get_ids

__all__ = ['make_data_fname', 'make_plot_fname', 'make_dirname', 'make_data_dirname']

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

    if where:
        data_fname = os.path.join(where, data_fname)

    if rel:
        data_fname = os.path.relpath(data_fname)

    if create:
        mkdir_p(os.path.dirname(data_fname))

    return data_fname


def make_plot_fname(ids, where='.', tag='', ext='.pdf', prefix='plot',
                    **kwargs):
    """
    Example:
        > make_plot_fname([1,2,3], where='Plots', tag='example')
        > 'Plot/data-1-2-3-example.dat'
    """
    return make_data_fname(ids, where, tag, ext, prefix, **kwargs)


# FIXME: I should be able to specify format
def make_dirname(ids, where='.', tag='', prefix='', sep='-', create=False):
    dirname = make_data_fname(ids, where=where, tag=tag, ext='', prefix='',
                    sep=sep, create=create)
    return dirname

make_data_dirname = make_dirname


# Mkdir -p functionality would be much easier with python 3
import errno    
import os

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
