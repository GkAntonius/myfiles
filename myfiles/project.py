from pathlib import Path
import shutil
from .config import ProjectConfig, RemoteHosts
from .nodeid import NodeID
from .node import Node
from .util import prompt_user_and_run, run_command, prompt_user_confirmation

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

    @staticmethod
    def _rsync_level(n: int):
        """
        Get rsync arguments to exclude directories past a certain depts.
        A level of zero means only the files in the specified directory.
        A level of one means include subdirectories, and so on.
        """
        arguments = []
        if n < 0 or n > 10:
            return arguments

        arguments.append("--exclude=" + (n+1)*"*/")
        return arguments
        
    def get_rsync_options(self,
                          level=1,
                          files_only=False,
                          with_filter=True,
                          dry_run=False,
                          **kwargs):
        """
        """
        arguments = ['-avh']
        if with_filter:
            arguments.append('-F')

        if dry_run:
            arguments.append('-n')

        if files_only:
            level=1
        arguments.extend(self._rsync_level(level))

        return arguments
        

    def pull_production_dir(self, hostname, ids, **kwargs):
        if hostname not in self.remote:
            raise Exception(f'Unknown host: {hostname}')

        node = Node(ids)
        tag = node.ids.tag
        rel_prod = self.production.relative_to(self.config.home)
        loc_prod = self.production.relative_to(Path().absolute())
        source = f"{hostname}:{rel_prod}/{tag}*"
        dest = f"{loc_prod}/"

        options = self.get_rsync_options(**kwargs)
        command_parts = ["rsync", source, dest] + options
        results = prompt_user_and_run(command_parts)

    def push_production_dir(self, hostname, ids, **kwargs):
        if hostname not in self.remote:
            raise Exception(f'Unknown host: {hostname}')

        node = Node(ids)
        if not node:
            raise Exception(f'Node not found: {ids}')

        tag = node.ids.tag
        rel_prod = self.production.relative_to(self.config.home)
        loc_prod = self.production.relative_to(Path().absolute())

        options = self.get_rsync_options(**kwargs)
        command_parts = ["rsync",
                        f"{loc_prod}/{tag}*",
                        f"{hostname}:{rel_prod}/",
                        ] + options
        result = prompt_user_and_run(command_parts)

    def pull_scratch(self, ids, **kwargs):

        node = Node(ids)

        tag = str(node.ids.tag)
        source = self.scratch / self.production.relative_to(self.topdir)
        dest = self.production

        options = self.get_rsync_options(**kwargs)
        command_parts = ["rsync", f"{source}/{tag}*", f"{dest}/"] + options
        results = prompt_user_and_run(command_parts)

    def push_scratch(self, ids, **kwargs):

        node = Node(ids)
        if not node:
            raise Exception(f'Node not found: {ids}')

        tag = str(node.ids.tag)
        source = self.production
        dest = self.scratch / self.production.relative_to(self.topdir)

        options = self.get_rsync_options(**kwargs)
        command_parts = ["rsync", f"{source}/{tag}*", f"{dest}/"] + options
        results = prompt_user_and_run(command_parts)

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

        source = self.local_data
        dest = self.local_data.relative_to(self.config.home)

        command_parts = ["rsync", f"{source}/", f"{hostname}:{dest}"] + options
        return prompt_user_and_run(command_parts)

    def push_global_data(self, hostname, **kwargs):
        if hostname not in self.remote:
            raise Exception(f'Unknown host: {hostname}')

        source = self.global_data
        dest = self.global_data.relative_to(self.config.home)

        command_parts = ["rsync", f"{source}/", f"{hostname}:{dest}"] + options
        return prompt_user_and_run(command_parts)

    @classmethod
    def new_project(cls, name, mkdir=True):
        config = ProjectConfig(path=Path('~'))
        config.name = name
        new = cls(config=config)

        if mkdir:
            if new.topdir.exists():
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
            new.make_scratch_link()

        return new

    def make_scratch_link(self):
        source = self.scratch 
        dest = self.topdir / 'scratch'

        command_parts = ["ln", "-nsf", str(source), str(dest)]
        return prompt_user_and_run(command_parts)
