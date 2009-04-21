from zohmg.utils import fail


class Config(object):
    # TODO: multiple dataset files
    config_file = "config/datasets.yaml"

    def __init__(self):
        self.config = {}
        self.__read_config()

    def __read_config(self):
        import yaml
        try:
            f = open(self.config_file, "r")
            self.config = yaml.load(f)
            f.close()
            return self.config
        except IOError, ioe:
            msg = "E: Could not read %s. %s." % (self.config_file,ioe.strerror)
            fail(msg,ioe.errno)

    def project_name(self):
        return self.config['project_name']

    def dimensions(self):
        return self.config['dimensions']

    def units(self):
        return self.config['units']

    def projections(self):
        return self.config['projections']
