import importlib.util

from importlib.abc import InspectLoader
from . import path


class Loader(InspectLoader):

    def __init__(self, app):
        self.app = app

    def get_source(self, fullname):
        return importlib.util.decode_source(self.source_bytes(fullname))

    def is_package(self, fullname):
        return path.contains(f"{fullname}.__init__", self.app)

    def path(self, fullname):
        if self.is_package(fullname):
            return path.from_package_name(fullname) + '__init__.py'
        return path.from_module_name(fullname)

    def source_bytes(self, fullname):
        try:
            return self.app.read(self.path(fullname))
        except KeyError:
            raise ImportError(f"No module: {fullname}", name=fullname)
