#!/usr/bin/python
import os, sys, yaml

def usage():
    print "usage: " + sys.argv[0] + " <map.py> <dumboesque arguments>"

# open problems:
#  do not read config inside mapperwrapper.
#  send user's mapper inside file.
#  keep 'all'-records.

# questions:
#  what will the queries look like?



# TMP
class config(object):
    config_file = "config.yaml"
    def __init__(self):
        self.config = {}
        self.has_read = False
    def read_config(self):
        import yaml
        f = open(self.config_file, "r")
        self.config = yaml.load(f)
        self.has_read = True
        f.close()
        # TODO: sanity check config.
        return config
    def sanity_check(self):
        return True
    def requested_projections(self):
        if not self.has_read:
            self.read_config()
        rps = []
        for unit in self.config['units']:
            for projection_name in self.config['units'][unit]:
                rps.append(self.config['units'][unit][projection_name])
                # FIXME: req.proj. are saved for all units for the time being..
        return rps


# TODO: send the user's mapper with -file and call it, say, 'mapper.py'. then we can do "import mapper" and be done.
def suck_in(path):
    # FIXME: sort of an ugly hack atm.
    sys.path.append(".")
    return __import__(path.split(".")[0]) # will not work if there are dots in the path.

# wrap user's mapper.
# FIXME: this is retard-slow.
def mapper_wrapper(m):
    def g(k,v):
        requested_projections = config().requested_projections()
        for r in m(k, v): # for every line of output from the user's mapper..
            ts, dims, units = r
            for u in units:  # ..and for every unit..
                for req in requested_projections:
                    # ..we yield data points for the projections requested.
                    newdims = {}
                    for d in req: # copy part of the full dimension.
                        newdims[d] = dims[d]
                    yield (ts, newdims, u), units[u]
    return g

# we'll pass the output of the reducer along to HBaseOutputReader.
def reducer(k, vs):
    import simplejson as json
    ts, dims, unit = k
    value = sum(vs)

    # TODO: only save the projections which the user care about.
    # ..do we want to filter that in the mapperwrapper perhaps?
    c = config()
    c.read_config()
    okcfs = []
    for unit in c.config['units']:
        for p in c.config['units'][unit]:
            projection = '-'.join(c.config['units'][unit][p])
            okcfs.append(projection)

    # rowkey is "unit-ymd"
    rk = '-'.join([unit, str(ts)])
    # column-family and qualifier; labels and values of projection.
    cf = '-'.join(dims.keys())
    q  = '-'.join(dims.values())
    
    if not cf in okcfs:
        sys.stderr.write("dropping cf: %s\n" % cf)
        return
    else:
        #sys.stderr.write("keeping cf: %s\n" % cf)
        pass

    yield (rk, json.dumps({cf+":"+q : {'value':value}}))


# tmp copy
# this is the user's mapper.
def m(key, value):
    from lfm.data.parse import web

    try: log = web.Log(value)
    except ValueError: return
    ua = web.UserAgent()

    ts = log.timestamp.ymd()
    dimensions = {'country'   : log.country(),
                  'domain'    : log.domain,
                  'useragent' : ua.classify(log.agent),
                  'usertype'  : ("user", "anon")[log.userid == None]
                  }
    values = {'pageviews' : 1}

    yield ts, dimensions, values



if __name__ == "__main__":
    envkey="ZOHMG_USER_MAPPER"
    user_mapper = os.getenv(envkey)
    #if user_mapper == None:
    if False:
        # first time around, it seems.
        try:
            mapper=sys.argv[1]
        except IndexError:
            usage()
            sys.exit(1)
        os.putenv(envkey, mapper)
        print "arguments are: %s" % str(sys.argv)
        print "sending: %s" % sys.argv[2:]
        os.system("dumbo start %s %s" % (sys.argv[0], " ".join(sys.argv[2:])))
    else:
        # dumbo started us. thanks for that.
        import dumbo
        #m = suck_in(user_mapper)
        #dumbo.run(mapper_wrapper(m.map), reducer)
        dumbo.run(mapper_wrapper(m), reducer)

