from pathlib import Path
import configparser
import json

CONFIG_FILENAME = '.myfilesrc'

class UserConfig(dict):

    # These define a directory structure
    user_defaults = {
        'Global': {
            'projects' : '~/Projects',
            'scratch' : '~/Scratch',
            'data' : '~/Data',
            },
        'Local': {
            'data' : 'Data',
            'production' : 'Production',
            'analysis' : 'Analysis',
            'results' : 'Results',
            },
        'Data': {
            'structure' : 'Structures',
            'pseudo' : 'Pseudos',
            },
        }

    header_tag = 'myfiles user confiuration'
    _config_filename = '.myfilesrc'

    def __init__(self, read=True, path='.', **kwargs):
        super().__init__()
        self.update(self.defaults)
        self.update(kwargs)
        self.files_read = []

        if not read:
            return self

        fnames = self.find_all_config_files(path)

        self.files_read.extend(fnames)

        config = configparser.ConfigParser()
        config.read(fnames)
        for sk in self.defaults:
            for key in self.defaults[sk]:
                try:
                    self[sk][key] = config[sk][key]
                except KeyError:
                    continue

    @property
    def defaults(self):
        return dict(self.user_defaults)

    @property
    def home(self):
        return Path('~').expanduser().absolute()
    
    @property
    def filename(self):
        return self.home / self._config_filename

    @property
    def projectsdir(self):
        return Path(self['Global']['projects']).expanduser().absolute()

    @property
    def global_scratch(self):
        return Path(self['Global']['scratch']).expanduser().absolute()

    @property
    def global_data(self):
        return Path(self['Global']['data']).expanduser().absolute()

    @property
    def file_exists(self):
        return self.filename.exists()

    @classmethod
    def find_all_config_files(cls, workdir):
        home = Path('~').expanduser().absolute()
        fnames = []
        workdir = Path(workdir).expanduser().absolute()
        p = workdir / cls._config_filename
        if p.exists():
            fnames.append(str(p))
        for parent in workdir.parents:
            p = parent / cls._config_filename
            if p.exists():
                fnames.append(str(p))
            if parent.resolve() == home.resolve():
                break
        fnames.reverse()
        return fnames

    def write(self, fname):
        config = configparser.ConfigParser()
        for sk in self.defaults:
            d = {}
            for key in self.defaults[sk]:
                d[key] = str(self[sk][key])
            config[sk] = d

        with open(fname, 'w') as configfile:
            config.write(configfile)

    def write_config_file(self, target=None):
        """Will not overwrite an existing file."""
        target = target or self.filename
        if not target.exists():
            answer = input(f"File '{target}' does not exist. \n"
                           "Do you want to write a new one? [y/N]: ")
    
            if answer.lower().startswith('y'):
                self.write(str(target))
                print(f"Wrote file '{target}'.")
                return self
            else:
                print(f"No file written.")

        return self

    def __str__(self):
        S  = ''
        n = len(self.header_tag) * 2
        S += n*'=' + '\n'
        S += self.header_tag + '\n'
        S += n*'-' + '\n'
        S += 'Files read: \n'
        for fname in self.files_read:
            S += str(Path(fname).absolute()) + '\n'
        S += n*'-' + '\n'

        d = json.dumps(dict(self))
        json_object = json.loads(d)
        S += json.dumps(json_object, indent=2) + '\n'
        S += n*'=' + '\n'
        return S

        #for sk in self.defaults:
        #    for key in self.defaults[sk]:
        #        val = self[sk][key]
        #        S += f"{key} = {repr(val)}\n"
        #return S


class ProjectConfig(UserConfig):

    project_defaults = {
        'Project': {
            'name' : 'UnknownProjectName',
            },
    }

    header_tag = 'myfiles project confiuration'

    @property
    def defaults(self):
        d = dict(self.user_defaults)
        d.update(self.project_defaults)
        return d

    @property
    def topdir(self):
        return self.projectsdir / self['Project']['name']

    @property
    def local_data(self):
        return self.topdir / self['Local']['data']

    @property
    def file_exists(self):
        topdir = self.find_topdir()
        if not topdir.exists():
            return False
        target = topdir / self._config_filename
        return target.exists()

    def write(self, fname):
        config = configparser.ConfigParser()
        for sk in self.project_defaults:
            d = {}
            for key in self.project_defaults[sk]:
                d[key] = str(self[sk][key])
            config[sk] = d

        with open(fname, 'w') as configfile:
            config.write(configfile)

    def write_config_file(self):
        """Will not overwrite an existing file."""
        topdir = self.find_topdir()
        if not topdir.exists():
            return
        target = topdir / self._config_filename
        super().write_config_file(target)

    def find_topdir(self):
        if self['Project']['name'] == self.defaults['Project']['name']:
            p = Path().absolute().relative_to(self.projectsdir)
            name = p.parts[0]
            self['Project']['name'] = name

        if not self.topdir.exists():
            print(f'Warning: top directory does not exist:\n {topdir}')

        return self.topdir


class RemoteHosts(UserConfig):

    project_defaults = {
        'Remotehosts': {
            'name' : 'HOSTNAME',
            },
    }

