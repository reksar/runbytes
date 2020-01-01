import io
import sys
import runpy
import base64
import zipfile
import importlib.abc
from zipimport import _bootstrap_external, path_sep, _zip_searchorder, _is_dir
from zipimport import _compile_source, _module_type
import pkgutil
from log import log


APP = 'UEsDBBQAAAAAAMJLn08AAAAAAAAAAAAAAAAIAAAAc3VicGFjay9QSwMEFAAAAAAAQkqfTwC1Hl5KAAAASgAAAAsAAABfX21haW5fXy5weWZyb20gc3VicGFjayBpbXBvcnQgY2FsYwppbXBvcnQgcHJpbnRlcgoKcHJpbnRlci5wcmludGVyKGNhbGMuY2FsYygxLCAyKSkKUEsDBBQAAAAAAMZ7NkwAAAAAAAAAAAAAAAALAAAAX19pbml0X18ucHlQSwMEFAAAAAAAr0mfT04xl30mAAAAJgAAAAoAAABwcmludGVyLnB5ZGVmIHByaW50ZXIoKmFyZ3MpOgogICAgcHJpbnQoKmFyZ3MpCgpQSwMEFAAAAAAAxns2TAAAAAAAAAAAAAAAABMAAABzdWJwYWNrL19faW5pdF9fLnB5UEsDBBQAAAAAAMZKn08wEEw9RgAAAEYAAAAPAAAAc3VicGFjay9jYWxjLnB5ZnJvbSAuIGltcG9ydCBoZWxwZXIKCmRlZiBjYWxjKHgsIHkpOgogICAgcmV0dXJuIHggKyB5ICsgaGVscGVyLnooeCkKClBLAwQUAAAAAABySp9PDLHwmRwAAAAcAAAAEQAAAHN1YnBhY2svaGVscGVyLnB5ZGVmIHooeCk6CiAgICByZXR1cm4gMiAqIHgKClBLAQIUAxQAAAAAAMJLn08AAAAAAAAAAAAAAAAIAAAAAAAAAAAAEADtQQAAAABzdWJwYWNrL1BLAQIUAxQAAAAAAEJKn08AtR5eSgAAAEoAAAALAAAAAAAAAAAAAACkgSYAAABfX21haW5fXy5weVBLAQIUAxQAAAAAAMZ7NkwAAAAAAAAAAAAAAAALAAAAAAAAAAAAAACkgZkAAABfX2luaXRfXy5weVBLAQIUAxQAAAAAAK9Jn09OMZd9JgAAACYAAAAKAAAAAAAAAAAAAACkgcIAAABwcmludGVyLnB5UEsBAhQDFAAAAAAAxns2TAAAAAAAAAAAAAAAABMAAAAAAAAAAAAAAKSBEAEAAHN1YnBhY2svX19pbml0X18ucHlQSwECFAMUAAAAAADGSp9PMBBMPUYAAABGAAAADwAAAAAAAAAAAAAApIFBAQAAc3VicGFjay9jYWxjLnB5UEsBAhQDFAAAAAAAckqfTwyx8JkcAAAAHAAAABEAAAAAAAAAAAAAAKSBtAEAAHN1YnBhY2svaGVscGVyLnB5UEsFBgAAAAAHAAcAnQEAAP8BAAAAAA=='
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


def _get_module_path(self, fullname):
    return fullname.replace('.', path_sep)


def _get_module_info(self, fullname):
    path = _get_module_path(self, fullname)
    for suffix, isbytecode, ispackage in _zip_searchorder:
        fullpath = path + suffix
        if fullpath in self._files:
            return ispackage
    return None

# Given a path to a Zip archive, build a dict, mapping file names
# (local to the archive, using SEP as a separator) to toc entries.
#
# A toc_entry is a tuple(
#  __file__,        # value to use for __file__
#  compress,        # compression kind; 0 for uncompressed
#  data_size,       # size of compressed data on disk
#  file_size,       # size of decompressed data
#  file_offset,     # offset of file header from start of archive
#  time,            # mod time of file (in dos format)
#  date,            # mod data of file (in dos format)
#  crc,             # crc checksum of the data
# )
#
# Directories can be recognized by the trailing path_sep in the name,
# data_size and file_offset are 0.
def read_files(self, archive):
    with zipfile.ZipFile(self.bytes_io) as app:
        files = {}
        for info in app.infolist():
            name = info.filename.replace('/', path_sep)
            path = _bootstrap_external._path_join(archive, name)
            compress = info.compress_type
            data_size = info.compress_size
            file_size = info.file_size
            file_offset = info.header_offset
            time = info.date_time
            date = info.date_time
            crc = info.CRC
            t = (path, compress, data_size, file_size, file_offset, time, date, crc, info)
            files[name] = t
        return files


def _get_data(self, fullpath):
    with zipfile.ZipFile(self.bytes_io) as pyz:
        return pyz.read(fullpath)


# Get the code object associated with the module specified by 'fullname'.
def _get_module_code(self, fullname):
    path = _get_module_path(self, fullname)
    for suffix, isbytecode, ispackage in _zip_searchorder:
        fullpath = path + suffix
        try:
            toc_entry = self._files[fullpath]
        except KeyError:
            pass
        else:
            modpath = toc_entry[0]
            data = _get_data(self, fullpath)
            if isbytecode:
                code = _unmarshal_code(self, modpath, fullpath, fullname, data)
            else:
                code = _compile_source(modpath, data)
            if code is None:
                continue
            modpath = toc_entry[0]
            return code, ispackage, modpath
    else:
        raise ImportError(f"Can't find module {fullname!r}", name=fullname)


class BytesImporter:
    """Inspired by zipimporter"""
    def __init__(self, path):
        """Used as a path hook"""
        app_bytes = base64.b64decode(APP)
        self.bytes_io = io.BytesIO(app_bytes)
        self.prefix = ''
        self.archive = path
        self._files = read_files(self, path)

    def find_loader(self, fullname, path=None):
        """
        Search for a module specified by 'fullname', a fully qualified (dotted)
        module name. It returns this instance itself if the module was found,
        a string containing the full path name if it's possibly a portion of a
        namespace package, or None otherwise.
        The optional 'path' argument is ignored - it's there for compatibility
        with the importer protocol.
        """
        mi = _get_module_info(self, fullname)
        if mi is not None:
            # This is a module or package.
            return self, []

        # Not a module or regular package. See if this is a directory, and
        # therefore possibly a portion of a namespace package.

        # We're only interested in the last path component of fullname
        # earlier components are recorded in self.prefix.
        modpath = _get_module_path(self, fullname)
        if _is_dir(self, modpath):
            # This is possibly a portion of a namespace
            # package. Return the string representing its path,
            # without a trailing separator.
            return None, [f'{self.archive}{path_sep}{modpath}']

        return None, []

    def get_code(self, fullname):
        """get_code(fullname) -> code object.

        Return the code object for the specified module. Raise ImportError
        if the module couldn't be found.
        """
        code, ispackage, modpath = _get_module_code(self, fullname)
        return code

    def load_module(self, fullname):
        """load_module(fullname) -> module.

        Load the module specified by 'fullname'. 'fullname' must be the
        fully qualified (dotted) module name. It returns the imported
        module, or raises ImportError if it wasn't found.
        """
        code, ispackage, modpath = _get_module_code(self, fullname)
        mod = sys.modules.get(fullname)
        if mod is None or not isinstance(mod, _module_type):
            mod = _module_type(fullname)
            sys.modules[fullname] = mod
        mod.__loader__ = self

        try:
            if ispackage:
                # add __path__ to the module *before* the code gets executed
                path = _get_module_path(self, fullname)
                fullpath = _bootstrap_external._path_join(self.archive, path)
                mod.__path__ = [fullpath]

            if not hasattr(mod, '__builtins__'):
                mod.__builtins__ = __builtins__
            _bootstrap_external._fix_up_module(mod.__dict__, fullname, modpath)
            exec(code, mod.__dict__)
        except:
            del sys.modules[fullname]
            raise

        try:
            mod = sys.modules[fullname]
        except KeyError:
            raise ImportError(f'Loaded module {fullname!r} not found in sys.modules')
        return mod


sys.path_hooks.append(BytesImporter)
#importer = pkgutil.get_importer(APP_ORIGIN)
runpy.run_path(APP_ORIGIN)

