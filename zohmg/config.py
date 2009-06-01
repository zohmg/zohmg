from zohmg.utils import fail # heh.
import os, re, sys, time


# the configuration file has four parts:
#   'dataset' - string
#   'dimensions' - list of strings
#   'units' - list of strings
#   'projections' - list of lists


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

        config_loaded    = False
        possible_configs = [self.config_file, "config/"+self.config_file]
        file_loaded = None

        # two error conditions can occur:
        #  A) all files missing/can't be opened. => try next file, report later.
        #  B) a file opens, but can't be parsed. => report imm.

        while (not config_loaded and len(possible_configs) > 0):
            config_file = possible_configs.pop()

            try:
                f = open(config_file, "r")
            except IOError, e:
                continue # try to open the next file.

            # we managed to open the file; will not try and open any more.
            # now, load yaml.
            try:
                self.config = yaml.load(f)
                file_loaded = config_file
            except yaml.scanner.ScannerError, e:
                # condition B.
                # report error immediately.
                sys.stderr.write("Configuration error: could not parse %s.\n" % config_file)
                sys.stderr.write("%s\n", e)
                f.close()
                sys.exit(1)

            # ok, good!
            f.close()
            config_loaded = True


        if not config_loaded:
            # condition A.
            sys.stderr.write("Configuration error: Could not read dataset configuration " \
                              "from any of these files:\n" \
                              "\n".join(a) + "\n")
            sys.exit(1)

        # check contents.
        if not self.sanity_check():
            msg = "[%s] Configuration error: Could not parse configuration from %s." % (time.asctime(), file_loaded)
            fail(msg) # TODO: should maybe not use fail as it raises SystemExit.

        return self.config


    def dataset(self):
        return self.config['dataset']
    def dimensions(self):
        return self.config['dimensions']
    def units(self):
        return self.config['units']
    def projections(self):
        # turn list of strings into list of list of strings.
        # ['country', 'country-domain-useragent-usertype']
        # => [['country'], ['country', 'domain', 'useragent', 'usertype']]
        return map(lambda s : s.split('-'), self.config['projections'])

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
            print >>sys.stderr, "[%s] Configuration error: Missing definition of dataset, dimensions, units, projections." \
                                % time.asctime()
            return False

        # dimensions, projections and units must be non-empty.
        if ds == None or us == None or ps == None or \
            len(ds) == 0 or len(us) == 0 or len(ps) == 0:
                print >>sys.stderr, "[%s] Configuration error: dimensions, projections and units must be non-empty." \
                                    % time.asctime()
                return False

        # also, the configuration may not reference unknown dimensions.
        for p in ps:
            for d in p:
                if d not in ds:
                    print >>sys.stderr, "[%s] Configuration error: %s is a reference to an unkown dimension." \
                        % (time.asctime(),d)
                    sane = False

        # also, there must be no funny characters in the name of the dataset, the dimensions or units.
        for (type, data) in [('dataset', [dataset]), ('dimension', ds), ('unit', us)]:
            for d in data:
                m = re.match('^[a-zA-Z0-9]+$', d)
                if m == None:
                    print >>sys.stderr, "[%s] Configuration error: '%s' is an invalid %s name." \
                                        % (time.asctime(), d, type)
                    sane = False

        return sane


class Environ(object):
    def __init__(self):
        self.environ = {}
        self.read_environ()

    def get(self, key):
        try:
            return self.environ[key]
        except:
            return ''

    def read_environ(self):
        # add config path so we can import from it.
        sys.path.append(".")
        sys.path.append("config")

        try:
            import environment
        except ImportError:
            msg = "[%s] Error: Could not import environment.py" % time.asctime()
            fail(msg)

        for key in dir(environment):
            self.environ[key] = environment.__dict__[key]
