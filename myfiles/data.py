from pathlib import Path
from .config import UserConfig, ProjectConfig

class DataDir:
    """A single data directory, containing subdirectories and files."""

    def __init__(self, dirname, config):
        self.config = config or ProjectConfig()
        self.dirname = Path(dirname).expanduser().absolute()
        self.pseudo_subdir = '.'

    @property
    def pseudo_dir(self):
        return self.dirname / self.config['Data']['pseudo']

    @property
    def structure_dir(self):
        return self.dirname / self.config['Data']['structure']

    def get_pseudo_dir(self, subdir=None, keywords=()):
        """
        Return the absolute path of a pseudopotentials directory that exists.
        Raise an exception if not found.
        """
        if subdir is not None:
            path = self.pseudo_dir / subdir
        elif not keywords:
            path = self.pseudo_dir
        else:
            directories = []
            counts = []
            for (dirpath, dirnames, filenames) in self.pseudo_dir.walk():
                if not dirnames:
                    continue
                counts = []
                for dirname in dirnames:
                    n = 0
                    for kw in keywords:
                        if kw.lower() in dirname.lower():
                            n += 1
                    directories.append(dirpath / dirname)
                    counts.append(n)

            nmax = max(counts)
            if nmax < len(keywords):
                print(nmax, len(keywords))
                raise Exception('Did not find pseudo directory matching keywords.')

            for dirpath, n in zip(directories, counts):
                if n == nmax:
                    path = dirpath
                    break

        #subdir = subdir or self.pseudo_subdir
        #path = self.pseudo_dir / subdir
        if not path.exists():
            raise Exception(f'Directory not found: {path}')
        return str(path.absolute())

    def get_pseudo(self, psps:[str], subdir=None, keywords=()):
        """
        Return the absolute path of a list of pseudopotentials files
        that exist.
        Raise an exception if not found.
        """
        path = Path(self.get_pseudo_dir(subdir=subdir, keywords=keywords))
        pseudo = []
        for psp in psps:
            fname = path / psp
            if not fname.exists():
                raise Exception(f'File not found: {fname}')
            pseudo.append(str(fname.absolute()))
        return pseudo


    def get_structure_dir(self):
        """
        Return the absolute path of the structure directory.
        Raise an exception if it does not exist.
        """
        if not self.structure_dir.exists():
            raise Exception(f'Directory does not exist: {self.structure_dir}')
        return str(self.structure_dir)

    def get_structure(self, filename):
        """
        Find the absolute path of a structure that exists.
        Raise an exception if not found.
        """
        #path = self.structure_dir / filename
        #if not path.exists():
        #    raise Exception(f'File not found: {path}')
        #return str(path.absolute())

        for ddf in self.structure_dir.walk():
            (dirpath, dirnames, filenames) = ddf
            for fname in filenames:
                if fname == filename:
                    return (dirpath / filename)

        raise Exception(f'File not found: {filename}')



class DataDirs(list):
    """
    A collection of data directories to search in,
    in order of decreasing priority.
    """

    def __init__(self, config=None):
        super().__init__()
        self.config = config or ProjectConfig()
        for dirname in (
                self.config.local_data, self.config.global_data):
            self.append(DataDir(dirname, self.config))

    def set_pseudo_subdir(self, subdir='.'):
        for datadir in self:
            datadir.pseudo_subdir = subdir

    def get_structure(self, filename):
        for datadir in self:
            try:
                return datadir.get_structure(filename)
            except:
                continue
        raise Exception(f'File not found: {filename}')

    def get_pseudo(self, psps, subdir=None, keywords=()):
        for datadir in self:
            try:
                return datadir.get_pseudo(psps, subdir=subdir, keywords=keywords)
            except:
                continue
        raise Exception(f'Files not found: {psps}')

    def get_structure_dir(self):
        for datadir in self:
            try:
                return datadir.get_structure_dir()
            except:
                continue
        raise Exception(f'File not found: {filename}')

    def get_pseudo_dir(self, subdir=None, keywords=()):
        for datadir in self:
            try:
                return datadir.get_pseudo_dir(subdir, keywords=keywords)
            except:
                continue
        raise Exception(f'Directory not found: {subdir}, {keywords}')
