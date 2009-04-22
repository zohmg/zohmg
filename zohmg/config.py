from zohmg.utils import fail
import os, sys, re

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


# TODO: multiple dataset files
class Config(object):
    def __init__(self, config_file=None):
        if yaml:
            self.config_file = config_file
        else:
            self.config_file = config_path + "dataset.yaml"

        self.config = {}
        self.__read_config()

    def __read_config(self):
        import yaml
        try:
            f = open(self.config_file, "r")
            self.config = yaml.load(f)
            f.close()
        except IOError, ioe:
            msg = "Error: Could not read %s. %s." % (self.config_file, ioe.strerror)
            fail(msg, ioe.errno)

        #if not self.sanity_check():
        #    # (how) do we force the caller to sanity check?
        #    # throw exception?
        #    pass

        return self.config


    def dataset(self):
        return self.config['dataset']
    def dimensions(self):
        return self.config['dimensions']
    def units(self):
        return self.config['units']
    def projections(self):
        return self.config['projections']

    # returns True if configuration is sane,
    # False otherwise.
    def sanity_check(self):
        sane = True # .. so far.
        try:
            # must be able to read these.
            dataset = self.dataset()
            ds = self.dimensions()
            us = self.units()
            ps = self.projections()
        except:
            # might as well return straight away; nothing else will work.
            sys.stderr.write("hey!, you must define 'dataset', 'dimensions', 'units' and 'projections'.\n")
            return False

        # dimensions, projections and units must be non-empty.
        if ds == None or us == None or ps == None or \
           len(ds) == 0 or len(us) == 0 or len(ps) == 0:
            sys.stderr.write("hey!, dimensions, projections and units must be non-empty\n")
            return False

        # also, the configuration may not reference unknown dimensions.
        for p in ps:
            if ps[p] == None or len(ps[p]) == 0:
                sys.stderr.write("hey!, you may not specify empty projections.\n")
                return False
            for d in ps[p]:
                if d not in ds:
                    sys.stderr.write("hey!, '%s' is a reference to an unknown dimension.\n" % d)
                    sane = False

        # also, there must be no funny characters in
        # the name of the dataset, the dimensions or units.
        for xs in [[dataset], ds, us]:
            for x in xs:
                m = re.match('^[a-zA-Z]+$', x)
                if m == None:
                    sys.stderr.write("hey!, '%s' is an invalid name.\n" % x)
                    sane = False

        # all is fine!
        return sane


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
