from importlib.abc import PathEntryFinder
from importlib.machinery import ModuleSpec
from . import path
from .loader import Loader


class Finder(PathEntryFinder):

    def __init__(self, app):
        self.app = app

    def find_spec(self, fullname, target=None):
        # TODO: implement target finder
        if path.contains(fullname, self.app):
            return self.module_spec(fullname)

    def module_spec(self, fullname):
        loader = Loader(self.app)
        is_package = loader.is_package(fullname)

        if is_package:
            origin_path = path.from_package_name
        else:
            origin_path = path.from_module_name

        origin = f"{self.app.name}/{origin_path(fullname)}"

        spec = ModuleSpec(
            fullname,
            loader,
            origin=origin,
            is_package=is_package,
        )

        if is_package:
            spec.submodule_search_locations.append(origin)

        return spec
