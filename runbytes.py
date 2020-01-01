import io
import sys
import runpy
import base64
import zipfile
import importlib.abc
import pkgutil
from log import log


APP = 'UEsDBBQAAAAAAMJLn08AAAAAAAAAAAAAAAAIAAAAc3VicGFjay9QSwMEFAAAAAAAQkqfTwC1Hl5KAAAASgAAAAsAAABfX21haW5fXy5weWZyb20gc3VicGFjayBpbXBvcnQgY2FsYwppbXBvcnQgcHJpbnRlcgoKcHJpbnRlci5wcmludGVyKGNhbGMuY2FsYygxLCAyKSkKUEsDBBQAAAAAAMZ7NkwAAAAAAAAAAAAAAAALAAAAX19pbml0X18ucHlQSwMEFAAAAAAAr0mfT04xl30mAAAAJgAAAAoAAABwcmludGVyLnB5ZGVmIHByaW50ZXIoKmFyZ3MpOgogICAgcHJpbnQoKmFyZ3MpCgpQSwMEFAAAAAAAxns2TAAAAAAAAAAAAAAAABMAAABzdWJwYWNrL19faW5pdF9fLnB5UEsDBBQAAAAAAMZKn08wEEw9RgAAAEYAAAAPAAAAc3VicGFjay9jYWxjLnB5ZnJvbSAuIGltcG9ydCBoZWxwZXIKCmRlZiBjYWxjKHgsIHkpOgogICAgcmV0dXJuIHggKyB5ICsgaGVscGVyLnooeCkKClBLAwQUAAAAAABySp9PDLHwmRwAAAAcAAAAEQAAAHN1YnBhY2svaGVscGVyLnB5ZGVmIHooeCk6CiAgICByZXR1cm4gMiAqIHgKClBLAQIUAxQAAAAAAMJLn08AAAAAAAAAAAAAAAAIAAAAAAAAAAAAEADtQQAAAABzdWJwYWNrL1BLAQIUAxQAAAAAAEJKn08AtR5eSgAAAEoAAAALAAAAAAAAAAAAAACkgSYAAABfX21haW5fXy5weVBLAQIUAxQAAAAAAMZ7NkwAAAAAAAAAAAAAAAALAAAAAAAAAAAAAACkgZkAAABfX2luaXRfXy5weVBLAQIUAxQAAAAAAK9Jn09OMZd9JgAAACYAAAAKAAAAAAAAAAAAAACkgcIAAABwcmludGVyLnB5UEsBAhQDFAAAAAAAxns2TAAAAAAAAAAAAAAAABMAAAAAAAAAAAAAAKSBEAEAAHN1YnBhY2svX19pbml0X18ucHlQSwECFAMUAAAAAADGSp9PMBBMPUYAAABGAAAADwAAAAAAAAAAAAAApIFBAQAAc3VicGFjay9jYWxjLnB5UEsBAhQDFAAAAAAAckqfTwyx8JkcAAAAHAAAABEAAAAAAAAAAAAAAKSBtAEAAHN1YnBhY2svaGVscGVyLnB5UEsFBgAAAAAHAAcAnQEAAP8BAAAAAA=='
APP_ORIGIN = 'app.pyz'


class Loader(importlib.abc.SourceLoader):
    def __init__(self):
        pass

    def get_data(path):
        return base64.b64decode(APP)

    def get_filename(fullname):
        return APP_ORIGIN


class Finder(importlib.abc.PathEntryFinder):
    def __init__(self, loader):
        self.loader = loader

    def find_spec(fullname, target=None):
        return importlib.machinery.ModuleSpec(
                APP_ORIGIN, AppLoader, origin=APP_ORIGIN, is_package=True)

    @classmethod
    def path_hook(cls, path_entry):
        return Finder


sys.path_hooks.append()
importer = pkgutil.get_importer(APP_ORIGIN)
log(importer)
#runpy.run_path(APP_ORIGIN)

