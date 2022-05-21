from base64 import b64decode
from io import BytesIO
from zipfile import PyZipFile


class App:

    separator = ':'

    def __init__(self, encoded_app: str):
        self.name, self.body = encoded_app.split(self.separator)

    @property
    def pyz_context(self):
        return PyZipFile(BytesIO(b64decode(self.body)))

    @property
    def path_entries(self):
        with self.pyz_context as pyz:
            return pyz.namelist()

    def read(self, path):
        with self.pyz_context as pyz:
            return pyz.read(path)
