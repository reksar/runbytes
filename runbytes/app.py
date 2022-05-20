class App:

    separator = ':'

    def __init__(self, encoded_app: str):
        self.name, self.body = encoded_app.split(self.separator)

