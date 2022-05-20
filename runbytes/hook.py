from .finder import Finder


class Hook:
    """Path Hook for search the `app`"""

    def __init__(self, app):
        self.app = app

    def __call__(self, path_entry):
        if path_entry.startswith(self.app.name):
            return Finder(self.app)
        raise ImportError(f"No path {path_entry}", path=path_entry)
