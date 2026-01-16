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

    def get_pseudo_dirs(self, keywords=('pbe','psp8','sr')):
        """
        Return a list of pseudopotential directories that exist
        and whose name contain some keywords.
        """

        # FIXME: A directory may match, but not contain any files

        matching_paths = []
        if not keywords:
            if self.pseudo_dir.exists():
                matching_paths.append(self.pseudo_dir.absolute())
            return matching_paths

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
            return matching_paths

        nmax = max(counts)
        #if nmax < len(keywords):
        #    print(nmax, len(keywords))
        #    #raise Exception('Did not find pseudo directory matching keywords.')
        #    return matching_paths

        for dirpath, n in zip(directories, counts):
            if n == nmax:
                matching_paths.append(dirpath.absolute())
                #path = dirpath
                #break

        #subdir = subdir or self.pseudo_subdir
        #path = self.pseudo_dir / subdir
        #if not path.exists():
        #    #raise Exception(f'Directory not found: {path}')
        #    return ScanResult.failure, ''

        return matching_paths

    def get_pseudo_dir(self, keywords=('pbe','psp8','sr')):
        dirs = self.get_pseudo_dirs(keywords=keywords)
        if not dirs:
            raise Exception('Could not find pseudopotential directory '
                            'with keywords: {keywords}')
        return dirs[0]

    def get_pseudopotentials(self, psps:[str],
                             keywords=('pbe','psp8','sr'),
                             path=None,
                             as_dict=False,
                             basename=False) -> ([str], [ScanResult]):
        """
        Return a list or dictionary of pseudopotential files.
        """

        if path is None:
            paths = self.get_pseudo_dirs(keywords=keywords)
        elif isinstance(path, (str, Path)):
            paths = [Path(path).absolute()]
        elif '__iter__' in dir(path):
            paths = [Path(p).absolute() for p in path]
        else:
            try:
                paths = [Path(path).absolute()]
            except:
                raise Exception('Invalid type for path: {}'.format(type(path)))

        N = len(psps)
        elements = [os.path.splitext(str(psp))[0] for psp in psps]
        pseudos = dict()
        results = []

        for element in elements:
            fname = ''
            res = ScanResult.failure

            for path in paths:
                search = path.glob(f'{element}.*')
                try:
                    filepath = next(search)
                except StopIteration:
                    continue

                if basename:
                    fname = filepath.name
                    res = ScanResult.success
                    break
                else:
                    fname = str(filepath.absolute())
                    res = ScanResult.success
                    break

            pseudos[element] = fname
            results.append(res)

        if not as_dict:
            pseudos = list(pseudos.values())

        return pseudos, results

    def get_structure_dir(self):
        """
        Return the absolute path of the structure directory.
        Raise an exception if it does not exist.
        """
        if not self.structure_dir.exists():
            raise Exception(f'Directory does not exist: {self.structure_dir}')
        return str(self.structure_dir)

    def get_structure_file(self, filename) -> (ScanResult, str):
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

        return ScanResult.failure, str(dirpath)

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

    def get_structure_file(self, filename):
        result = ScanResult.no_scan
        for datadir in self:
            result, filepath = datadir.get_structure_file(filename)
            if result == ScanResult.success:
                return filepath
        if result == ScanResult.no_scan:
            raise Exception('No data directory to scan.')
        else:
            for datadir in self:
                print(datadir)
            raise Exception(f'File not found: {filename}')

    def get_pseudo_dirs(self, keywords=('pbe','psp8','sr')):
        dirs = []
        for datadir in self:
            dirs.extend(datadir.get_pseudo_dirs(keywords=keywords))
        return dirs

    def get_pseudo_dir(self, keywords=('pbe','psp8','sr')):
        dirs = self.get_pseudo_dirs(keywords=keywords)
        if not dirs:
            raise Exception('Could not find pseudopotential directory '
                            'with keywords: {keywords}')
        return dirs[0]

    def get_pseudopotentials(self, psps:[str],
                             keywords=('pbe','psp8','sr'),
                             path=None,
                             as_dict=False,
                             basename=False) -> [str]:

        N = len(psps)
        elements = [os.path.splitext(str(psp))[0] for psp in psps]
        pseudos = dict()
        results = N * [ScanResult.failure]

        for datadir in self:
            ps, res = datadir.get_pseudopotentials(
                psps=psps, keywords=keywords, path=path,
                as_dict=True, basename=basename)

            for i, el in enumerate(elements):
                if (results[i] == ScanResult.failure
                    and res[i] == ScanResult.success):

                    pseudos[el] = ps[el]
                    results[i] = ScanResult.success

            if all([r == ScanResult.success for r in results]):
                break

        if any([r == ScanResult.failure for r in results]):

            # Get some info for debugging
            if path is not None:
                if isinstance(path, (str, Path)):
                    directories = [Path(path).absolute()]
                if '__iter__' in dir(path):
                    directories = [Path(p).absolute() for p in path]
            else:
                directories = self.get_pseudo_dirs(keywords=keywords)
            directories = [str(d) for d in directories]

            msg = "Pseudopotential file not found.\n"
            msg += f'psps = {psps} \n'
            msg += f'keywords = {keywords} \n'
            msg += f'Search directories: \n'
            for d in directories:
                msg += f'{d} \n'
            raise Exception(msg)

        if not as_dict:
            pseudos = list(pseudos.values())

        return pseudos

    def get_structure_dir(self):
        for datadir in self:
            try:
                return datadir.get_structure_dir()
            except:
                continue
        raise Exception(f'File not found: {filename}')

    #def get_pseudo_dir(self, *args, **kwargs):
    #    result = ScanResult.no_scan
    #    for datadir in self:
    #        result, path = datadir.get_pseudo_dir(*args, **kwargs)
    #        if result == ScanResult.success:
    #            return path

    #    if result == ScanResult.no_scan:
    #        raise Exception('No data directory to scan.')
    #    else:
    #        raise Exception(f'Directory not found: {args}')

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
