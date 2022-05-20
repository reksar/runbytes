import importlib.machinery

from . import path
from .loader import Loader


class Finder(importlib.abc.PathEntryFinder):

    def __init__(self, app):
        self.app = app

    def find_spec(self, fullname, target=None):
        # TODO: implement target finder
        if path.contains(fullname, self.app):
            loader = Loader(self.app)
            is_package = loader.is_package(fullname)
            origin = path.from_package_name(fullname) if is_package else path.from_module_name(fullname)
            origin = f"{self.app.name}/{origin}"
            spec = importlib.machinery.ModuleSpec(fullname, loader, origin=origin, is_package=is_package)
            if is_package:
                spec.submodule_search_locations.append(origin)
            return spec
