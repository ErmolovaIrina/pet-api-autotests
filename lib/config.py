import yaml

class Config:

    def __init__(self):
        self.data = None
        self.base_url = None

    def load(self, filename):
        with open(filename) as f:
            self.data = yaml.safe_load(f)
            self.base_url = str(self.data["url"])