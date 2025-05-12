from pathlib import Path
import configparser

class UserConfig:

    user_defaults = {
        'Global': {
            'global_projects_dir' : '~/Projects/',
            'global_scratch_dir', : '~/Scratch/',
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

    @property
    def sections(self):
        return dict(self.user_defaults)

    def __init__(self):
        for sk in self.sections:
            for key in self.sections[sk]:
                setattr(self, key, self.sections[sk][key])

    def from_config_file(cls, fname=None):
        if fname is None:
            fname = Path('~/.myfilesrc')
            #fname_local = Path('.myfilesrc')
        else:
            fname = Path(fname)

        if not fname.exists():
            raise Exception(str(fname) + " does not exist.")

        new = cls()

        config = configparser.ConfigParser()
        config.read(fname)
        for sk in self.sections:
            for key in self.sections[sk]:
                setattr(new, key, config[sk][key])

        return new

    def write(self, fname):
        config = configparser.ConfigParser()
        for sk in self.sections:
            for key in self.sections[sk]:
                config[sk][key] = str(getattr(self, key))

        with open(fname, 'w') as configfile:
            config.write(configfile)

    def __str__(self):
        S  = 'myfiles user confiuration\n'
        S += '-------------------------\n'
        for sk in self.sections:
            for key in self.sections[sk]:
                val = getattr(self, key)
                S += f"{key}={val}\n"
        return S


class ProjectConfig(UserConfig):

    project_defaults = {
        'Project': {
            'name' : 'ProjectName',
            'topdir' : '~/Projects/ProjectName',
            },

    @property
    def sections(self):
        d = dict(self.user_defaults)
        d.update(self.project_defaults)
        return d

