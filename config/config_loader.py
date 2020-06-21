"""
The config loader
"""

import json


class Loader:
    def __init__(self, file):
        # load config in memory
        config = open("config/" + file, 'r')
        self.config = json.load(config)
        config.close()
        print("Loading config")

    def __getitem__(self, item):
        # define a way to navigate the config item
        return self.config[item]
