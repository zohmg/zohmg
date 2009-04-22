from zohmg.utils import fail
import os, sys

# TODO: is it a safe assumption that HADOOP_HOME is in os.environ when
# running dumbo?
# ALSO: is it safe to assume that HADOOP_HOME is *not* defined when
# running locally?
# TODO: why are we doing this in a global variable?
# figure out if we are run inside dumbo.
# files shipped to dumbo are all put in cwd.
if "HADOOP_HOME" in os.environ:
    config_path = ""
else:
    config_path = "config/"


class Config(object):
    # TODO: multiple dataset files
    config_file = config_path+"dataset.yaml"

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

    def dataset(self):
        return self.config['dataset']
    def dimensions(self):
        return self.config['dimensions']
    def units(self):
        return self.config['units']
    def projections(self):
        return self.config['projections']

class Environ(object):
    def __init__(self):
        self.environ = {}
        self.read_environ()

    def get(self,key):
        return self.environ[key]

    def read_environ(self):
        sys.path.append("") # add cwd so we can import from it.
        try:
            env = __import__(config_path+"environment")
        except ImportError, ioe:
            msg = "E: Could not import %senvironment.py. %s." % (config_path,ioe.strerror)
            fail(msg,ioe.errno)

        for key in dir(env):
            self.environ[key] = env.__dict__[key]
