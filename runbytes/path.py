def from_name(fullname):
    return fullname.replace('.', '/')


def from_module_name(fullname):
    return f"{from_name(fullname)}.py"


def from_package_name(fullname):
    return f"{from_name(fullname)}/"


def contains(fullname, app):
    path_entries = app.path_entries
    package_path = from_package_name(fullname)
    module_path = from_module_name(fullname)
    return package_path in path_entries or module_path in path_entries
