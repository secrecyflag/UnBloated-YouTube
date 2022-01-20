import json


class Settings:
    def __init__(self, path=None, file=None):
        self.path = path if path is not None else "settings.json"
        self.file = open(self.path) if file is None else file
        self.settings = json.load(self.file)
    
    def write(self):
        self.file.close()
        with open(self.path, "w+") as file:
            json.dump(self.settings, file, indent=4)
        self.open()
    
    def get_default_quality(self):
        return self.settings["defaultQuality"]

    def write_settings(self, settings: dict):
        for key in settings:
            self.settings[key] = settings[key][0]
        self.write()

    def open(self):
        self.file = open(self.path)

    def close(self):
        self.file.close()

