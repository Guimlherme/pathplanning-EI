import json

class Configs:
    def __init__(self, filename='config.json'):
        with open("config.json", "r") as f:
            self.config = json.load(f)
    
    def get_setting(self, name):
        return self.config[name]
    
    def set_setting(self, name, value):
        self.config[name] = value