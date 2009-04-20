import yaml

class Config(object):
    config_file = "config.yaml"
    def __init__(self):
        self.config = {}
        self.has_config = False
        self.read_config()
    def read_config(self):
        f = open(self.config_file, "r")
        self.config = yaml.load(f)
        self.has_config = True
        f.close()
        if not self.sanity_check():
            return {} # TODO: throw exception, yes?
        return self.config
    def sanity_check(self):
        # TODO.
        return True
    def project_name(self):
        return self.config['project_name']
    def dimensions(self):
        return self.config['dimensions']
    def units(self):
        return self.config['units']
    def projections(self):
        return self.config['projections']
