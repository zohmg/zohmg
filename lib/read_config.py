#!/usr/bin/python

import yaml

class config(object):
    config_file = "config/config.yaml"
    def __init__(self):
        self.config = {}
    def read_config(self):
        f = open(self.config_file, "r")
        self.config = yaml.load(f)
        f.close()
        # TODO: sanity check config.
        return config

    def sanity_check(self):
        return True
