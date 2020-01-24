import io
import sys
import runpy
import base64
import zipfile
import importlib.abc
import importlib.util
import importlib.machinery
from log import log


APP = 'UEsDBBQAAAAAAMJLn08AAAAAAAAAAAAAAAAIAAAAc3VicGFjay9QSwMEFAAAAAAAQkqfTwC1Hl5KAAAASgAAAAsAAABfX21haW5fXy5weWZyb20gc3VicGFjayBpbXBvcnQgY2FsYwppbXBvcnQgcHJpbnRlcgoKcHJpbnRlci5wcmludGVyKGNhbGMuY2FsYygxLCAyKSkKUEsDBBQAAAAAAMZ7NkwAAAAAAAAAAAAAAAALAAAAX19pbml0X18ucHlQSwMEFAAAAAAAr0mfT04xl30mAAAAJgAAAAoAAABwcmludGVyLnB5ZGVmIHByaW50ZXIoKmFyZ3MpOgogICAgcHJpbnQoKmFyZ3MpCgpQSwMEFAAAAAAAxns2TAAAAAAAAAAAAAAAABMAAABzdWJwYWNrL19faW5pdF9fLnB5UEsDBBQAAAAAAMZKn08wEEw9RgAAAEYAAAAPAAAAc3VicGFjay9jYWxjLnB5ZnJvbSAuIGltcG9ydCBoZWxwZXIKCmRlZiBjYWxjKHgsIHkpOgogICAgcmV0dXJuIHggKyB5ICsgaGVscGVyLnooeCkKClBLAwQUAAAAAABySp9PDLHwmRwAAAAcAAAAEQAAAHN1YnBhY2svaGVscGVyLnB5ZGVmIHooeCk6CiAgICByZXR1cm4gMiAqIHgKClBLAQIUAxQAAAAAAMJLn08AAAAAAAAAAAAAAAAIAAAAAAAAAAAAEADtQQAAAABzdWJwYWNrL1BLAQIUAxQAAAAAAEJKn08AtR5eSgAAAEoAAAALAAAAAAAAAAAAAACkgSYAAABfX21haW5fXy5weVBLAQIUAxQAAAAAAMZ7NkwAAAAAAAAAAAAAAAALAAAAAAAAAAAAAACkgZkAAABfX2luaXRfXy5weVBLAQIUAxQAAAAAAK9Jn09OMZd9JgAAACYAAAAKAAAAAAAAAAAAAACkgcIAAABwcmludGVyLnB5UEsBAhQDFAAAAAAAxns2TAAAAAAAAAAAAAAAABMAAAAAAAAAAAAAAKSBEAEAAHN1YnBhY2svX19pbml0X18ucHlQSwECFAMUAAAAAADGSp9PMBBMPUYAAABGAAAADwAAAAAAAAAAAAAApIFBAQAAc3VicGFjay9jYWxjLnB5UEsBAhQDFAAAAAAAckqfTwyx8JkcAAAAHAAAABEAAAAAAAAAAAAAAKSBtAEAAHN1YnBhY2svaGVscGVyLnB5UEsFBgAAAAAHAAcAnQEAAP8BAAAAAA=='
APP_ORIGIN = 'app.pyz'


class Reader:

    @staticmethod
    def open_pyz():
        pyz_bytes = base64.b64decode(APP)
        pyz_io = io.BytesIO(pyz_bytes)
        return zipfile.PyZipFile(pyz_io)

    @staticmethod
    def path_entries():
        with Reader.open_pyz() as pyz:
            return pyz.namelist()

    @staticmethod
    def read(path):
        with Reader.open_pyz() as pyz:
            return pyz.read(path)


class Path:

    @staticmethod
    def from_name(fullname):
        return fullname.replace('.', '/')

    @staticmethod
    def from_module_name(fullname):
        return f'{Path.from_name(fullname)}.py'

    @staticmethod
    def from_package_name(fullname):
        return f'{Path.from_name(fullname)}/'

    @staticmethod
    def is_contains(fullname):
        # TODO: move it somewhere
        path_entries = Reader.path_entries()
        package_path = Path.from_package_name(fullname)
        module_path = Path.from_module_name(fullname)
        return package_path in path_entries or module_path in path_entries


class Loader(importlib.abc.InspectLoader):

    def get_source(self, fullname):
        is_package = self.is_package(fullname)
        path = Path.from_package_name(fullname) + '__init__.py' if is_package else Path.from_module_name(fullname)
        try:
            source_bytes = Reader.read(path)
        except KeyError:
            raise ImportError(f'no module {fullname}', name=fullname)
        return importlib.util.decode_source(source_bytes)

    def is_package(self, fullname):
        return Path.is_contains(f'{fullname}.__init__')


class Finder(importlib.abc.PathEntryFinder):
    def __init__(self):
        self.loader = Loader()

    def find_spec(self, fullname, target=None):
        # TODO: implement target finder
        if Path.is_contains(fullname):
            is_package = self.loader.is_package(fullname)
            origin = Path.from_package_name(fullname) if is_package else Path.from_module_name(fullname)
            origin = f'{APP_ORIGIN}/{origin}'
            spec = importlib.machinery.ModuleSpec(fullname, self.loader, origin=origin, is_package=is_package)
            if is_package:
                spec.submodule_search_locations.append(origin)
            return spec

    def path_hook(self, path_entry):
        if path_entry.startswith(APP_ORIGIN):
            return self
        raise ImportError(f'no path {path_entry}', path=path_entry)


finder = Finder()
sys.path_hooks.append(finder.path_hook)
runpy.run_path(APP_ORIGIN)
