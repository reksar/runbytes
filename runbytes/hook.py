from .finder import Finder


def hook(app_name, app):
    return lambda path_entry: path_hook(path_entry, app_name, app)

def path_hook(path_entry, app_name, app):
    if path_entry.startswith(app_name):
        return Finder(app_name, app)
    raise ImportError(f"No path {path_entry}", path=path_entry)
