import os
from pathlib import Path

from .util import ScanResult
from .config import UserConfig, ProjectConfig

class DataDir:
    """A single data directory, containing subdirectories and files."""

    def __init__(self, dirname, config):
        self.config = config or ProjectConfig()
        self.dirname = Path(dirname).expanduser().absolute()
        self.pseudo_subdir = '.'

    def __str__(self):
        return f"Datadir({self.dirname})"

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

        # FIXME: A directory may match, but not contain any files (or contain

        if subdir is not None:
            path = self.pseudo_dir / subdir
        elif not keywords:
            path = self.pseudo_dir
        else:
            directories = []
            counts = []
            # GA: Temporarily backtracking to python 3.11 compatible version.
            #for (dirpath, dirnames, filenames) in self.pseudo_dir.walk():
            for root, dirnames, filenames in os.walk(str(self.pseudo_dir)):
                dirpath = Path(root)
                if not dirnames:
                    continue
                for dirname in dirnames:
                    n = 0
                    for kw in keywords:
                        if kw.lower() in dirname.lower():
                            n += 1
                    directories.append(dirpath / dirname)
                    counts.append(n)

            if not directories:
                return ScanResult.failure, self.pseudo_dir

            nmax = max(counts)
            if nmax < len(keywords):
                print(nmax, len(keywords))
                #raise Exception('Did not find pseudo directory matching keywords.')
                return ScanResult.failure, ''

            for dirpath, n in zip(directories, counts):
                if n == nmax:
                    path = dirpath
                    break

        #subdir = subdir or self.pseudo_subdir
        #path = self.pseudo_dir / subdir
        if not path.exists():
            #raise Exception(f'Directory not found: {path}')
            return ScanResult.failure, ''

        return ScanResult.success, path.absolute()

    def get_pseudopotentials(self, psps:[str],
                             subdir=None,
                             keywords=(),
                             as_dict=False,
                             basename=False):
        """
        Return the absolute path of a list of pseudopotentials files
        that exist. Raise an exception if not found.
        """
        # FIXME: Should scan several matching directories.
        result, path = self.get_pseudo_dir(subdir=subdir, keywords=keywords)
        if result != ScanResult.success:
            return result, {}

        pseudos = dict()
        elements = [os.path.splitext(psp)[0] for psp in psps]

        for element in elements:
            search = path.glob(f'{element}.*')
            try:
                filepath = next(search)
            except StopIteration:
                return ScanResult.failure, {}

            if basename:
                pseudos[element] = filepath.name
            else:
                pseudos[element] = str(filepath.absolute())

        if not as_dict:
            pseudos = list(pseudos.values())

        return ScanResult.success, pseudos

    def get_structure_dir(self):
        """
        Return the absolute path of the structure directory.
        Raise an exception if it does not exist.
        """
        if not self.structure_dir.exists():
            raise Exception(f'Directory does not exist: {self.structure_dir}')
        return str(self.structure_dir)

    def get_structure(self, filename) -> (ScanResult, Path):
        """
        Find the absolute path of a structure that exists.
        """
        #path = self.structure_dir / filename
        #if not path.exists():
        #    raise Exception(f'File not found: {path}')
        #return str(path.absolute())

        # GA: Temporarily backtracking to python 3.11 compatible version.
        #for (dirpath, dirnames, filenames) in self.structure_dir.walk():
        dirpath = None
        for root, dirnames, filenames in os.walk(str(self.structure_dir)):
            dirpath = Path(root)
            for fname in filenames:
                if fname == filename:
                    return ScanResult.success, (dirpath / filename)

        return ScanResult.failure, dirpath

    def get_datafile(self, filename) -> (ScanResult, Path):
        """
        Find the absolute path of a data file that exists.
        """
        #path = self.structure_dir / filename
        #if not path.exists():
        #    raise Exception(f'File not found: {path}')
        #return str(path.absolute())

        # GA: Temporarily backtracking to python 3.11 compatible version.
        #for (dirpath, dirnames, filenames) in self.structure_dir.walk():
        for root, dirnames, filenames in os.walk(str(self.dirname)):
            dirpath = Path(root)
            for fname in filenames:
                if fname == filename:
                    return ScanResult.success, (dirpath / filename)

        return ScanResult.failure, dirpath

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
        result = ScanResult.no_scan
        for datadir in self:
            result, filepath = datadir.get_structure(filename)
            if result == ScanResult.success:
                return filepath
        if result == ScanResult.no_scan:
            raise Exception('No data directory to scan.')
        else:
            for datadir in self:
                print(datadir)
            raise Exception(f'File not found: {filename}')

    def get_pseudopotentials(self, *args, **kwargs):
        for datadir in self:
            result, pseudos = datadir.get_pseudopotentials(*args, **kwargs)
            if result == ScanResult.success:
                return pseudos

        if result == ScanResult.no_scan:
            raise Exception('No data directory to scan.')
        else:
            #msg = "Pseudopotential file not found.\n"
            #msg += f'Search pattern: {element}.* \n'
            #msg += f'Search directory: {path} \n'
            raise Exception(f'Files not found: {args[0]}')

    def get_structure_dir(self):
        for datadir in self:
            try:
                return datadir.get_structure_dir()
            except:
                continue
        raise Exception(f'File not found: {filename}')

    def get_pseudo_dir(self, *args, **kwargs):
        result = ScanResult.no_scan
        for datadir in self:
            result, path = datadir.get_pseudo_dir(*args, **kwargs)
            if result == ScanResult.success:
                return path

        if result == ScanResult.no_scan:
            raise Exception('No data directory to scan.')
        else:
            raise Exception(f'Directory not found: {args}')

    def get_datafile(self, filename):
        result = ScanResult.no_scan
        for datadir in self:
            result, filepath = datadir.get_datafile(filename)
            if result == ScanResult.success:
                return result, filepath
        return result, self.dirname
        #if result == ScanResult.no_scan:
        #    raise Exception('No data directory to scan.')
        #else:
        #    raise Exception(f'File not found: {filename}')
        #return result, Path
