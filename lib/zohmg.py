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
    def dimensions(self):
        if not self.has_config: self.read_config()
        return self.config['dimensions']
    def units(self):
        if not self.has_config: self.read_config()
        return self.config['units']
    def projections(self):
        if not self.has_config: self.read_config()
        return self.config['projections']

class Mapper():
    def __init__(self, usermapper):
        self.usermapper = usermapper
        self.projections = Config().projections()

    # wrapper around the user's mapper.
    def __call__(self, key, value):
        for r in self.usermapper(key, value):
            # for every yield from the user's mapper -- which represent a point in n-space -- 
            # we perform dimensionality reduction, yielding data points for all requested projections.
            ts, dims, units = r
            for u in units:
                for p in self.projections.values():
                    newdims = {}
                    for d in p:
                        newdims[d] = dims[d]
                    yield (ts, newdims, u), units[u]


class Reducer:
    def __init__(self):
        self.reduces = self.counters['reduces']
        self.config = Config()
    def __call__(self, key, values):
        self.reduces += 1
        ts, dims, unit = key
        value = sum(values)

        # rowkey: "unit-ymd".
        rk = '-'.join([unit, str(ts)])
        cf = '-'.join(dims.keys())
        q  = '-'.join(dims.values())

        # remember, we'll pass the output of this reducer to HBaseOutputReader.
        yield rk, json.dumps({cf+":"+q : {'value':value}})
