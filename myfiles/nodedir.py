from pathlib import Path
import shutil
from .config import UserConfig, ProjectConfig, NodeConfig, RemoteHosts
from .nodeid import NodeID
import subprocess

__all__ = ['NodeDir']

class NodeDir:
    """
    A directory containing directories or files of several nodes.
    """

    def __init__(self, dirname):
        self.path = Path(dirname)
        self.filename = self.path / '.myfilerc'

        self.nodes = []  # A list of NodeID objects.
        self.creation_date = []
        self.discovery_date = []

    def scan(self):
        if self.nodes:
            self.nodes = []
        for item in self.path.iterdir():
            if item.is_symlink():
                continue

            node = NodeID.from_path(self.path)
            if node:
                self.nodes.append(node)

        return self.nodes

    def __iter__(self):
        if not self.noderegistry:
            self.scan()

        for id in self.noderegistry:
            yield id

    #def display(self):
    #    pass

    def write_registry(self):
        pass

    def read_registry(self):
        pass
