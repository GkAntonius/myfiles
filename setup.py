

from __future__ import print_function
import os
import shutil

from setuptools import find_packages, setup


#---------------------------------------------------------------------------
# Basic project information
#---------------------------------------------------------------------------

name = 'myfiles'
description = """
My personal module to manage data file names.
"""
author = 'Gabriel Antonius'
license = 'All rights reserved (but who cares, really...)'
__version__ = '2.0.0'

#---------------------------------------------------------------------------
# Helper functions
#---------------------------------------------------------------------------

def cleanup():
    """Clean up the junk left around by the build process."""

    egg = '{}.egg-info'.format(name)
    try:
        shutil.rmtree(egg)
    except Exception as E:
        print(E)
        try:
            os.unlink(egg)
        except:
            pass

#---------------------------------------------------------------------------
# Setup
#---------------------------------------------------------------------------


setup_args = dict(
      name             = name,
      version          = __version__,
      description      = description,
      author           = author,
      license          = license,
      packages         = find_packages(),
      )

if __name__ == "__main__":
    setup(**setup_args)
    cleanup()

