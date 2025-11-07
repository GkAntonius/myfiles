from pathlib import Path
import configparser
from copy import copy, deepcopy
import json
import abc

from .util import prompt_user_and_run, run_command, prompt_user_confirmation

class Config(dict, abc.ABC):

    _config_filename = '.myfilesrc'

    def __init__(self, path='.', read=True, **kwargs):
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

    @property
    @abc.abstractmethod
    def defaults(self):
        return {}

    @property
    def home(self):
        return Path('~').expanduser().absolute()

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
        if home not in workdir.parents and home != workdir:
            p = home / cls._config_filename
            if p.exists():
                fnames.append(str(p))
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

    @property
    def filename(self):
        return self.home / self._config_filename

    @property
    def file_exists(self):
        return self.filename.exists()

    def write_config_file(self, target=None):
        """Will not overwrite an existing file."""
        target = target or self.filename
        if target.exists():
            answer = input(f"File '{target}' already exists. \n"
                           "Do you want to overwrite it? [y/N]: ")
    
            if answer.lower().startswith('y'):
                self.write(str(target))
                print(f"Wrote file '{target}'.")
                return self
            else:
                print(f"No file written.")
                return self

        self.write(str(target))
        return self

class UserConfig(Config):

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
    @property
    def defaults(self):
        return deepcopy(self.user_defaults)
    
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
    def global_scratch_projects(self):
        return self.global_scratch / self.projectsdir.relative_to(self.home)

    @property
    def global_scratch_data(self):
        return self.global_scratch / self.global_data.relative_to(self.home)

    def make_global_dirs(self):
        todo = []
        for directory in (self.projectsdir,
                          self.global_scratch,
                          self.global_data,
                          self.global_scratch_projects,
                          self.global_scratch_data,
                            ):
            if not directory.exists():
                todo.append(directory)

        if not todo:
            return

        msg = 'The following directories will be created:\n'
        msg += '\n'.join([str(d) for d in todo])
        prompt_user_confirmation(msg)
        for d in todo:
            d.mkdir(exist_ok=True)
                

# =========================================================================== #
# =========================================================================== #


class ProjectConfig(UserConfig):

    project_defaults = {
        'Project': {
            'name' : 'DefaultProjectName',
            },
    }

    header_tag = 'myfiles project confiuration'

    @property
    def is_default(self):
        return (self.name == self.project_defaults['Project']['name'])

    @property
    def defaults(self):
        d = deepcopy(self.user_defaults)
        d.update(deepcopy(self.project_defaults))
        return d

    @property
    def topdir(self):
        return self.projectsdir / self['Project']['name']

    @property
    def name(self):
        return self['Project']['name']

    @name.setter
    def name(self, value):
        self['Project']['name'] = value

    @property
    def filename(self):
        return self.topdir / self._config_filename

    @property
    def local_data(self):
        return self.topdir / self['Local']['data']

    @property
    def production(self):
        return self.topdir / self['Local']['production']

    @property
    def analysis(self):
        return self.topdir / self['Local']['analysis']

    @property
    def results(self):
        return self.topdir / self['Local']['results']

    @property
    def local_scratch(self):
        return self.global_scratch / self.topdir.relative_to(self.home)

    @property
    def scratch_production(self):
        return self.local_scratch / self.production.relative_to(self.topdir)

    @property
    def scratch_analysis(self):
        return self.local_scratch / self.analysis.relative_to(self.topdir)

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
        if self.is_default:
            try:
                p = Path().absolute().relative_to(self.projectsdir)
                name = p.parts[0]
                self['Project']['name'] = name
            except ValueError:
                pass
                #msg  = 20 * '=' + '\n'
                #msg += f'Error: Make sure you have a valid {self._config_filename} file.\n'
                #msg += 'Current path: ' + str(Path().absolute()) + '\n'
                #msg += 20 * '=' + '\n'
                #print(msg)
                #raise
                

        if not self.topdir.exists():
            print(f'Warning: top directory does not exist:\n {self.topdir}')

        return self.topdir

    def path_is_valid_project_topdir(self, path=None):
        if path is None:
            path = Path()
        else:
            path = Path(path)
        return (path.parent == self.projectsdir)


class NodeConfig(ProjectConfig):

    node_defaults = {
        'Node': {
            'name' : 'DefaultNodeName',
            'ndigids' : 3,
            },
    }

    @property
    def defaults(self):
        d = dict(self.user_defaults)
        d.update(self.project_defaults)
        d.update(self.node_defaults)
        return d


class RemoteHosts(Config):
    """
    Assume your ~/.ssh/config is set so that
    """
    remotehosts_defaults = {
        'RemoteHosts': {
            'hosts' : [], # Must be replaced at initialization
    #    # Should be a dict of dicts
    #    #   'narval': {'name' : 'narval'}
        },
    }

    header_tag = 'Remote hosts'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['RemoteHosts']['hosts'] = []
        
        # Manual parsing!
        sshconfig = Path('~/.ssh/config').expanduser().absolute()
        if sshconfig.exists():
            with open(str(sshconfig), 'r') as f:
                for line in f.readlines():
                    if line.startswith('Host'):
                        parts = line.split()
                        if len(parts) > 1:
                            self['RemoteHosts']['hosts'].append(parts[1])
            self.files_read.append(sshconfig)

    def find_all_config_files(self, path):
        return []

    @property
    def defaults(self):
        return deepcopy(self.remotehosts_defaults)

    @property
    def hosts(self):
        return self['RemoteHosts']['hosts']

    def __contains__(self, hostname):
        return (hostname in self.hosts)
    
    def write(self, fname):
        return

    def write_config_file(self, target=None):
        return

    def __str__(self):
        #S  = super().__str__()
        S = ''
        n = len(self.header_tag) * 2
        S += n*'=' + '\n'
        S += self.header_tag + '\n'
        S += n*'-' + '\n'
        S += 'Files read: \n'
        for fname in self.files_read:
            S += str(Path(fname).absolute()) + '\n'
        S += n*'-' + '\n'

        S += 'Remote hosts: \n'
        for host in self.hosts:
            S += f'    {host}\n'
        S += n*'=' + '\n'
        return S

