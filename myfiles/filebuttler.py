import os
import warnings

home = os.path.realpath(os.environ['HOME'])

_top_projects_dir_name = 'Work/Projects'


__all__ = ['FileButtler', 'fb', 'project_dir',
           'data_dir', 'production_dir', 'pseudo_dir', 'pseudos_dir', 'structure_dir', 'structures_dir']


def first_dir_after(path, top):
    """Return the first directory after top"""
    full_subdir = path.split(top)[-1]
    last = rest = full_subdir
    root = '/'
    while rest and rest != root:
        rest, last = os.path.split(rest)
    return last

class FileButtler(object):

    # This is the directory that contains all `project`  subdirectories.
    _top_projects_dir = os.path.realpath(os.path.join(home, _top_projects_dir_name))
    
    # These are other directories that may also contain a `project` subdirectory,
    registered_dirs = ('Production', 'Writing')

    def __init__(self, topdir=None):
        if topdir:
            self.find_project_dir(topdir)
        else:
            self.find_project_dir(self.curdir)

    def find_project_dir(self, dirname):
        if not dirname:
            dirname = self.curdir

        rdirname = os.path.realpath(dirname)

        if self._top_projects_dir in rdirname:
            project_name = first_dir_after(rdirname, self._top_projects_dir)
        else:
            for top in self.registered_dirs:
                if top in rdirname:
                    project_name = first_dir_after(rdirname, top)
                    break
            else:
                raise Exception('Could not find project dir!' + '\n'+ rdirname) 

        project_dir = os.path.join(self._top_projects_dir, project_name)
        if not os.path.exists(project_dir):
            #raise Exception('Could not find project dir!') 
            raise Exception('Could not find project dir!' + '\n'+ rdirname + '\n' + project_dir) 

        self._project_dir = project_dir
        return project_dir

    #def find_production_dir(self, 

    @property
    def curdir(self):
        return os.path.realpath(os.curdir)

    _project_dir = None
    @property
    def project_dir(self):
        if not self._project_dir:
            self._project_dir = self.find_project_dir()
        return self._project_dir

    @property
    def data_dir(self):
        return os.path.join(self.project_dir, 'Data')

    @property
    def structure_dir(self):
        return os.path.join(self.data_dir, 'Structures')

    @property
    def pseudo_dir(self):
        return os.path.join(self.data_dir, 'Pseudos')

    @property
    def production_dir(self):
        return os.path.join(self.project_dir, 'Production')

    @property
    def analysis_dir(self):
        return os.path.join(self.project_dir, 'Production')

    def find_pseudos(self, *pseudos, where='auto'):
        """
        Find one or many pseudopotential files.
        e.g. find_pseudos('Sr', 'Ti', 'O')
        """
        raise NotImplementedError

    def find_structure(self, ids=None, tag=None):
        """
        Find a structure file containing 
        e.g. find_pseudos('Sr', 'Ti', 'O')
        """
        raise NotImplementedError

    


# =========================================================================== #
"""Execution                                                                """
# =========================================================================== #

try:
    fb = FileButtler()
    project_dir = fb.project_dir
    data_dir = fb.data_dir
    production_dir = fb.production_dir
    pseudo_dir = fb.pseudo_dir
    pseudos_dir = pseudo_dir  # Alias
    structure_dir = fb.structure_dir
    structures_dir = structure_dir  # Alias
except Exception as e:
    fb = None
    project_dir = None
    data_dir = None
    production_dir = None
    pseudo_dir = None
    pseudos_dir = None
    structure_dir = None
    structures_dir = None
    warnings.warn('File Buttler could not locate project directory\n' + str(e))

