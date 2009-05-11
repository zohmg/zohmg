from zohmg.utils import fail
import os, re, sys, time

# TODO: is it a safe assumption that HADOOP_HOME is in os.environ when
# running dumbo?
# ALSO: is it safe to assume that HADOOP_HOME is *not* defined when
# running locally?
# TODO: why are we doing this in a global variable?

# figure out if we are run inside dumbo.
# files shipped to dumbo are all put in cwd.

# FIXME: $HADOOP_HOME can and will be set outside of hadoop jobs.
if "HADOOP_HOME" in os.environ:
    config_path = os.path.abspath("")
else:
    config_path = os.path.abspath("config/")


# TODO: multiple dataset files
class Config(object):
    def __init__(self, config_file=None):
        if config_file:
            self.config_file = config_file
        else:
            self.config_file = "dataset.yaml"

        self.config = {}
        self.__read_config()


    def __read_config(self):
        import yaml
        possible_configs = [self.config_file, "config/"+self.config_file]
        config_loaded = False
        for config_file in possible_configs:
            if config_loaded:
                continue
            try:
                f = open(config_file, "r")
                self.config = yaml.load(f)
                f.close()
                config_loaded = True
            except:
                pass

        if not config_loaded:
            msg = "[%s] Error: Could not read configuration." % time.asctime()
            fail(msg)

        if not self.sanity_check():
            msg = "[%s] Error: Could not parse configuration." % time.asctime()
            fail(msg)

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
            print >>sys.stderr, "[%s] Error: Data set: Missing definition of dataset, dimensions, units, projections." \
                                % time.asctime()
            return False

        # dimensions, projections and units must be non-empty.
        if ds == None or us == None or ps == None or \
            len(ds) == 0 or len(us) == 0 or len(ps) == 0:
                print >>sys.stderr, "[%s] Error: Data set: dimensions, projections and units must be non-empty." \
                                    % time.asctime()
                return False

        # also, the configuration may not reference unknown dimensions.
        for p in ps:
            if ps[p] == None or len(ps[p]) == 0:
                print >>sys.stderr, "[%s] Error: Data set: Empty projections are not allowed." % time.asctime()
                return False
            for d in ps[p]:
                if d not in ds:
                    print >>sys.stderr, "[%s] Error: Data set: %s is a reference to an unkown dimension." \
                                    % (time.asctime(),d)
                    sane = False # TODO: return False ?

        # also, there must be no funny characters in
        # the name of the dataset, the dimensions or units.
        for xs in [[dataset], ds, us]:
            for x in xs:
                m = re.match('^[a-zA-Z0-9]+$', x)
                if m == None:
                    print >>sys.stderr, "[%s] Error: Data set: '%s' is an invalid name." % (time.asctime(),x)
                    sane = False # TODO: return False ?

        return sane


class Environ(object):
    def __init__(self):
        self.environ = {}
        self.read_environ()

    def get(self,key):
        # FIXME: catch KeyError.
        return self.environ[key]

    def read_environ(self):
        # FIXME: think harder about paths; is environment.py really where you think it is?
        sys.path.append(config_path) # add config path so we can import from it.
        try:
            import environment
        except ImportError:
            msg = "[%s] Error: Could not import environment. %s." % (time.asctime(), config_path)
            fail(msg)

        for key in dir(environment):
            self.environ[key] = environment.__dict__[key]
