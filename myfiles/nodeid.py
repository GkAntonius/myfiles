import os
from pathlib import Path

class NodeID(list):
    """A sequence of digits identifying a node."""
    sep = '-'

    def __init__(self, ids: [int]):
        super().__init__(ids)

    def __str__(self):
        return self.sep.join(str(i) for i in self)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i, j in zip(self, other):
            if i != j:
                return False
        return True

    def __contains__(self, other):
        if len(other) < len(self):
            return False
        for i, j in zip(self, other):
            if i != j:
                return False
        return True

    def trim(self, n):
        if n > len(self):
            return self
        cls = type(self)
        return cls(self[:n])

    def partition(self, n):
        if n > len(self):
            return self, cls([])
        cls = type(self)
        return cls(self[:n]), cls(self[n:])

    def last(self, n):
        if n > len(self):
            return self
        cls = type(self)
        return cls(self[-n:])

    @classmethod
    def from_path(cls, path=None):
        """
        Read the ids from a file path.
        Extend the indices with each subdirectory.
        """
        if path is None:
            try:
                from __main__ import __file__ as mainfile

                # Special case, when called from this module's main function.
                from .__main__ import __file__ as localmainfile
                if mainfile == localmainfile:
                    return cls.from_path('.')

                return cls.from_path(mainfile)

            except:
                return cls.from_path('.')

        ids = list()
        rest = Path(path).expanduser().absolute()
        last = rest.name
        while last:
            ids_p = list(cls.read_ids(last))
            ids.extend(list(reversed(ids_p)))
            rest = rest.parent
            last = rest.name
        return cls(list(reversed(ids)))

    @classmethod
    def from_parent_path(cls, path=None):
        """
        Read the ids from the path parent, typically the directory hosting
        a file.
        """
        if path is None:
            try:
                from __main__ import __file__ as mainfile
                return cls.from_path(Path(mainfile).parent)
            except:
                return cls.from_path(Path().parent)
        else:
            return cls.from_path(Path(path).parent)

    @classmethod
    def read_ids(cls, fname):
        """Read the ids from a file basename."""
        basename = os.path.splitext(str(fname))[0]
        ids = list()
        for tok in basename.split(cls.sep):
            if tok.isdigit():
                ids.append(int(tok))
        x = basename.split(cls.sep)
        return cls(ids)

    from_str = read_ids

    def scan_directory(self, path):
        """
        Look for matching directories and files in a path.
        Return a list of all directories and files.
        """
        directories = []
        files = []

        for (dirpath, dirnames, filenames) in Path(path).walk():

            for filename in filenames:
                path = dirpath / filename
                pathID = self.from_path(path)
                if pathID in self:
                    files.append(str(path))

            to_remove = []
            for dirname in dirnames:
                path = dirpath / dirname
                #print(f'Scanning : {path}')  # DEBUG
                pathID = self.from_path(path)
                if (self not in pathID) and (pathID not in self):
                    to_remove.append(dirname)
                    continue

                if pathID in self:
                    directories.append(str(path) + '/')
                    # Stop iteration for directories we add.
                    if len(pathID) > len(self):
                        to_remove.append(dirname)
                        continue

            for dirname in to_remove:
                dirnames.remove(dirname)

        return directories, files

