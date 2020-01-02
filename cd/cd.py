import shutil
from dataclasses import dataclass
from os import chdir, getcwd, path
from tempfile import mkdtemp


@dataclass
class ChangeDirMeta:
    current: str
    previous: str


class cd:
    def __init__(self, directory=None):
        if directory is None:
            directory = path.realpath(mkdtemp())
            self.created = True
        else:
            self.created = False
        self.directory = directory

    def __enter__(self):
        return self.enter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit()

    def enter(self):
        self.original = getcwd()
        chdir(self.directory)
        return ChangeDirMeta(current=self.directory, previous=self.original)

    def exit(self):
        chdir(self.original)
        if self.created:
            shutil.rmtree(self.directory)
