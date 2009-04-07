#!/usr/bin/python
import yaml
import simplejson as json

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
        if not self.has_config: self.read_config()
        return self.config['project_name']
    def requested_projections(self):
        if not self.has_config: self.read_config()
        rps = []
        for projection_name in self.config['projections']:
            rps.append(self.config['projections'][projection_name])
        return rps

class Mapper():
    def __init__(self, usermapper):
        self.usermapper = usermapper
        self.requested_projections = Config().requested_projections()

    def __call__(self, key, value):
        # wrapper around the user's mapper.
        for r in self.usermapper(key, value):
            # for every yield from the user's mapper
            # we yield data points for all requested projections.
            ts, dims, units = r
            for u in units:
                for req in self.requested_projections:
                    newdims = {}
                    for d in req:
                        newdims[d] = dims[d]
                    yield (ts, newdims, u), units[u]


# we'll pass the output of the reducer along to HBaseOutputReader.
class Reducer:
    def __init__(self):
        self.reduces = self.counters['reduces']
        self.config = Config()
    def __call__(self, key, values):
        self.reduces += 1
        ts, dims, unit = key
        value = sum(values)

        # rowkey is "unit-ymd";
        rk = '-'.join([unit, str(ts)])
        # column-family and qualifier are label and value of dimensions.
        cf = '-'.join(dims.keys())
        q  = '-'.join(dims.values())

        yield rk, json.dumps({cf+":"+q : {'value':value}})




    #okcfs = []
    #for p in c.config['projections']:
    #    projection = '-'.join(c.config['projections'][p])
    #    okcfs.append(projection)

    #if not cf in okcfs:
    #    sys.stderr.write("dropping cf: %s\n" % cf)
    #    return
    #else:
    #    #sys.stderr.write("keeping cf: %s\n" % cf)
    #    pass



