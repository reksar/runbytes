import io
import base64
import zipfile


def open_pyz(app):
    pyz_bytes = base64.b64decode(app)
    pyz_io = io.BytesIO(pyz_bytes)
    return zipfile.PyZipFile(pyz_io)

def path_entries(app):
    with open_pyz(app) as pyz:
        return pyz.namelist()

def read(path, app):
    with open_pyz(app) as pyz:
        return pyz.read(path)
