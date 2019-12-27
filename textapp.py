import sys
import runpy
import base64
import importlib.abc


APP = 'UEsDBBQAAAAAAJhZkE9vCjQ3PQAAAD0AAAALAAAAX19tYWluX18ucHlpbXBvcnQgY2FsYwppbXBvcnQgcHJpbnRlcgoKcHJpbnRlci5wcmludGVyKGNhbGMuY2FsYygxLCAyKSkKUEsDBBQAAAAAAMZ7NkwAAAAAAAAAAAAAAAALAAAAX19pbml0X18ucHlQSwMEFAAAAAAAKFmQT1sITOEhAAAAIQAAAAcAAABjYWxjLnB5ZGVmIGNhbGMoeCwgeSk6CiAgICByZXR1cm4geCArIHkKUEsDBBQAAAAAABZZkE9OMZd9JgAAACYAAAAKAAAAcHJpbnRlci5weWRlZiBwcmludGVyKCphcmdzKToKICAgIHByaW50KCphcmdzKQoKUEsBAhQDFAAAAAAAmFmQT28KNDc9AAAAPQAAAAsAAAAAAAAAAAAAAKSBAAAAAF9fbWFpbl9fLnB5UEsBAhQDFAAAAAAAxns2TAAAAAAAAAAAAAAAAAsAAAAAAAAAAAAAAKSBZgAAAF9faW5pdF9fLnB5UEsBAhQDFAAAAAAAKFmQT1sITOEhAAAAIQAAAAcAAAAAAAAAAAAAAKSBjwAAAGNhbGMucHlQSwECFAMUAAAAAAAWWZBPTjGXfSYAAAAmAAAACgAAAAAAAAAAAAAApIHVAAAAcHJpbnRlci5weVBLBQYAAAAABAAEAN8AAAAjAQAAAAA='
APP_ORIGIN = 'app.pyz'


class AppLoader(importlib.abc.SourceLoader):

    @staticmethod
    def get_data(path):
        return base64.b64decode(APP)

    @staticmethod
    def get_filename(fullname):
        return APP_ORIGIN


class AppFinder(importlib.abc.PathEntryFinder):

    @staticmethod
    def find_spec(fullname, target=None):
        return importlib.machinery.ModuleSpec(
                APP_ORIGIN, AppLoader, origin=APP_ORIGIN, is_package=True)


def app_path_hook(path):
    if path != APP_ORIGIN:
        raise ImportError(f'Path must be an {APP_ORIGIN}', path=path)
    return AppFinder


sys.path_hooks.append(app_path_hook)
runpy.run_path(APP_ORIGIN)

