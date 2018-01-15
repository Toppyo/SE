
class Client:
    def __init__(self, no=None, name=None, level=None):
        self.no = no
        self.name = name
        self.level = level

    def get_name(self):
        return self.name

    def get_level(self):
        return self.level

    def create(self, no, name, level):
        self.no = no
        self.name = name
        self.level = level

