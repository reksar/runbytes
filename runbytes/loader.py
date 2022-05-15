import io
import base64
import zipfile
import importlib.abc
import importlib.util
import importlib.abc
import importlib.util

from . import path
from . import reader


class Loader(importlib.abc.InspectLoader):

    def __init__(self, app):
        self.app = app

    def get_source(self, fullname):
        is_package = self.is_package(fullname)
        app_path = path.from_package_name(fullname) + '__init__.py' if is_package else path.from_module_name(fullname)
        try:
            source_bytes = reader.read(app_path, self.app)
        except KeyError:
            raise ImportError(f"no module {fullname}", name=fullname)
        return importlib.util.decode_source(source_bytes)

    def is_package(self, fullname):
        return path.contains(f"{fullname}.__init__", self.app)
