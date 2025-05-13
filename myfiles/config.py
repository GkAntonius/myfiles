from pathlib import Path
import configparser

CONFIG_FILENAME = '.myfilesrc'

class UserConfig:

    user_defaults = {
        'Global': {
            'global_projects_dir' : '~/Projects/',
            'global_scratch_dir' : '~/Scratch/',
            'global_data_dir' : '~/Data',
            'global_pseudo_dir' : '~/Data/Pseudos',
            'global_structure_dir' : '~/Data/Structures',
            },
        'Local': {
            'local_data_dir' : 'Data',
            'local_pseudo_dir' : 'Data/Pseudos',
            'local_structure_dir' : 'Data/Structures',
            'local_production_dir' : 'Production',
            'local_analysis_dir' : 'Analysis',
            'local_plot_dir' : 'Plots',
            },
        }

    header_tag = 'myfiles user confiuration'

    def __init__(self):
        self.files_read = []
        for sk in self.sections:
            for key in self.sections[sk]:
                setattr(self, key, self.sections[sk][key])

    @property
    def sections(self):
        return dict(self.user_defaults)

    @classmethod
    def from_config_files(cls, fnames=None):

        if fnames is None:
            # Search for all configuration files in parent directories.
            fnames = []
            home = Path('~').expanduser().absolute()
            curdir = Path().absolute()
            p = curdir / CONFIG_FILENAME
            if p.exists():
                fnames.append(str(p))
            for parent in curdir.parents:
                p = parent / CONFIG_FILENAME
                if p.exists():
                    fnames.append(str(p))
                if parent.resolve() == home.resolve():
                    break

        elif isinstance(fnames, str):
            fnames = [fnames]
        else:
            fnames = list(fnames)

        #if not fname.exists():
        #    raise Exception(str(fname) + " does not exist.")

        new = cls()
        if not fnames:
            return new

        new.files_read.extend(fnames)

        config = configparser.ConfigParser()
        config.read(fnames)
        for sk in new.sections:
            for key in new.sections[sk]:
                setattr(new, key, config[sk][key])

        return new

    def write(self, fname):
        config = configparser.ConfigParser()
        for sk in self.sections:
            d = {}
            for key in self.sections[sk]:
                d[key] = str(getattr(self, key))
            config[sk] = d

        with open(fname, 'w') as configfile:
            config.write(configfile)

    def __str__(self):
        S  = ''
        n = len(self.header_tag)
        S += n*'-' + '\n'
        S += self.header_tag + '\n'
        for fname in self.files_read:
            S += str(Path(fname).absolute()) + '\n'
        S += n*'-' + '\n'

        for sk in self.sections:
            for key in self.sections[sk]:
                val = getattr(self, key)
                S += f"{key} = {repr(val)}\n"
        return S


class ProjectConfig(UserConfig):

    project_defaults = {
        'Project': {
            'name' : 'ProjectName',
            'topdir' : '~/Projects/ProjectName',
            },
    }

    header_tag = 'myfiles project confiuration'

    @property
    def sections(self):
        d = dict(self.user_defaults)
        d.update(self.project_defaults)
        return d

