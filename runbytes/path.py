import io
import base64
import zipfile
import importlib.abc
import importlib.util

from . import path
from . import reader


def from_name(fullname):
    return fullname.replace('.', '/')

def from_module_name(fullname):
    return f"{path.from_name(fullname)}.py"

def from_package_name(fullname):
    return f"{path.from_name(fullname)}/"

def contains(fullname, app):
    # TODO: move it somewhere
    path_entries = reader.path_entries(app)
    package_path = path.from_package_name(fullname)
    module_path = path.from_module_name(fullname)
    return package_path in path_entries or module_path in path_entries
