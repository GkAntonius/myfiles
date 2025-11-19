from pathlib import Path
import shutil
from .config import ProjectConfig, RemoteHosts
from .nodeid import NodeID
from .node import Node
from .util import (prompt_user_and_run, run_command, prompt_user_confirmation,
                   get_rsync_command_parts)

__all__ = ['Project']

class Project:

    def __init__(self, config=None, path='.'):
        config = config or ProjectConfig(path=path)
        self.config = config
        self.remote = RemoteHosts()
        self.name = str(config['Project']['name'])

    def __str__(self):
        S = ''
        header = f'Project {self.name}'
        n = 2 * len(header)
        S += n*'=' + '\n'
        S += header + '\n'
        S += f'Top directory: {self.topdir}\n'
        S += n*'-' + '\n'
        S += 'Configuration files: \n'
        for fname in self.config.files_read:
            S += str(Path(fname).absolute()) + '\n'
        S += n*'-' + '\n'
        S += f'Directories:\n'
        for p in (self.local_data,self.production,
                  self.analysis,self.results):
            S += f'    {p}\n'
        S += n*'=' + '\n'
        return S

    @property
    def topdir(self):
        return self.config.topdir

    @property
    def global_data(self):
        return self.config.global_data

    @property
    def local_data(self):
        return self.config.local_data

    @property
    def production(self):
        return self.config.production

    @property
    def analysis(self):
        return self.config.analysis

    @property
    def results(self):
        return self.config.results

    @property
    def scratch(self):
        return self.config.local_scratch

    @property
    def scratch_production(self):
        return self.config.scratch_production

    @property
    def scratch_analysis(self):
        return self.config.scratch_analysis

    def iter_dir_nodes(self, directory):
        """
        Look for nodes in a directory.
        """
        path = Path(directory)
        for dirname in path.iterdir():
            if not dirname.is_dir():
                continue
            node = Node.from_path(dirname, project=self)
            if not node:
                continue
            yield node

    def iter_production_nodes(self):
        return self.iter_dir_nodes(self.production)

    def iter_analysis_nodes(self):
        return self.iter_dir_nodes(self.analysis)

    def iter_results_nodes(self):
        path = Path(self.results)
        for fname in path.iterdir():
            node = Node.from_path(fname)
            if not node:
                continue
            yield node

    def make_directories(self):
        todo = []
        for directory in (self.topdir, self.local_data, self.production,
                        self.analysis, self.results, self.local_scratch,
                        self.scratch_production):
            if not directory.exists():
                todo.append(directory)

        if not todo:
            return

        msg = 'The following directories will be created:\n'
        msg += '\n'.join([str(d) for d in todo])
        prompt_user_confirmation(msg)
        for d in todo:
            d.mkdir(exist_ok=True)

    def pull_production_dir(self, hostname, ids, **kwargs):
        if hostname not in self.remote:
            raise Exception(f'Unknown host: {hostname}')

        node = Node(ids)
        tag = node.ids.tag
        rel_prod = self.production.relative_to(self.config.home)
        loc_prod = self.production.relative_to(Path().absolute())
        source = f"{hostname}:{rel_prod}/{tag}*"
        dest = f"{loc_prod}/"
        command_parts = get_rsync_command_parts(source, dest, **kwargs)
        return prompt_user_and_run(command_parts)

    def push_production_dir(self, hostname, ids, **kwargs):

        if hostname not in self.remote:
            raise Exception(f'Unknown host: {hostname}')

        node = Node(ids)
        if not node:
            raise Exception(f'Node not found: {ids}')

        tag = node.ids.tag
        rel_prod = self.production.relative_to(self.config.home)
        loc_prod = self.production.relative_to(Path().absolute())
        source = f"{loc_prod}/{tag}*"
        dest = f"{hostname}:{rel_prod}/"
        command_parts = get_rsync_command_parts(source, dest, **kwargs)
        return prompt_user_and_run(command_parts)

    def pull_scratch(self, ids, **kwargs):
        node = Node(ids)
        tag = str(node.ids.tag)
        sourcedir = self.scratch / self.production.relative_to(self.topdir)
        destdir = self.production
        source = f"{sourcedir}/{tag}*"
        dest = f"{destdir}/"
        command_parts = get_rsync_command_parts(source, dest, **kwargs)
        return prompt_user_and_run(command_parts)

    def push_scratch(self, ids, **kwargs):
        node = Node(ids)
        if not node:
            raise Exception(f'Node not found: {ids}')

        tag = str(node.ids.tag)
        sourcedir = self.production
        destdir = self.scratch / self.production.relative_to(self.topdir)
        source = f"{sourcedir}/{tag}*"
        dest = f"{destdir}/"
        command_parts = get_rsync_command_parts(source, dest, **kwargs)
        return prompt_user_and_run(command_parts)

    def copy_analysis_files_to_results(self, *args, **kwargs):
        """
        Look for files produced in analysis directory and copy them to
        the results directory.
        """
        for node in self.iter_analysis_nodes():
            node.scan_analysis()
            node.copy_analysis_files_to_results(*args, **kwargs)

    def push_local_data(self, hostname, **kwargs):
        if hostname not in self.remote:
            raise Exception(f'Unknown host: {hostname}')

        sourcedir = self.local_data
        destdir = self.local_data.relative_to(self.config.home)
        source = f"{sourcedir}/"
        dest = f"{hostname}:{destdir}"
        command_parts = get_rsync_command_parts(source, dest, **kwargs)
        return prompt_user_and_run(command_parts)

    def push_global_data(self, hostname, **kwargs):
        if hostname not in self.remote:
            raise Exception(f'Unknown host: {hostname}')

        sourcedir = self.global_data
        destdir = self.global_data.relative_to(self.config.home)
        source = f"{sourcedir}/"
        dest = f"{hostname}:{destdir}"
        command_parts = get_rsync_command_parts(source, dest, **kwargs)
        return prompt_user_and_run(command_parts)

    @classmethod
    def new_project(cls, name_or_path, mkdir=True):
        config = ProjectConfig(path=Path('~'))

        p = Path(name_or_path)
        prel = p.absolute().relative_to(config.projectsdir)

        if p.name == name_or_path:
            config.name = p.name

        elif (not p.absolute().is_relative_to(config.projectsdir)
              or (prel.name != str(prel))):
            raise Exception(
                'Requested path for new project must be in the Projects '
                'directory: ' + str(config.projectsdir))
        else:
            config.name = prel.name

        new = cls(config=config)

        if mkdir:
            if new.topdir.exists() and new.config.file_exists:
                import warnings
                warnings.warn(f'Project already exists: {new.topdir}')

            print(new.topdir)
            new.topdir.mkdir(exist_ok=True)
            new.config.write_config_file()

            for dirname in (new.local_data, new.production,
                            new.analysis, new.results):
                print(dirname)
                dirname.mkdir(exist_ok=True)

        if new.config.global_scratch.exists():
            new.scratch.mkdir(exist_ok=True)
            new.make_scratch_link(prompt=False)

        return new

    def make_scratch_link(self, prompt=True):
        source = self.scratch 
        dest = self.topdir / 'scratch'
        command_parts = ["ln", "-nsf", str(source), str(dest)]
        if prompt:
            return prompt_user_and_run(command_parts)
        else:
            return run_command(command_parts)
