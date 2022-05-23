from base64 import b64decode
from io import BytesIO
from zipfile import PyZipFile


class App:

    def __init__(self, encoded_app: str):
        self.name, self.payload = encoded_app.split(':')

    @property
    def pyz_context(self):
        return PyZipFile(BytesIO(b64decode(self.payload)))

    @property
    def path_entries(self):
        with self.pyz_context as pyz:
            return pyz.namelist()

    def read(self, path):
        with self.pyz_context as pyz:
            return pyz.read(path)
