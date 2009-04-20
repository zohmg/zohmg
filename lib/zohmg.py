#!/usr/bin/env python

import os, sys
import yaml
import simplejson as json
from utils import *

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


class Environment(object):
    def __init__(self):
        self.environ = {}
        self.read_environ()

    def get(self,key):
        return self.environ[key]

    def read_environ(self):
        sys.path.append("") # add cwd
        try:
            env = __import__("config/environment")
        except ImportError:
            print >> sys.stderr,"E: Could not import config/environment.py, does it exist?"
            exit(1)

        for key in dir(env):
            self.environ[key] = env.__dict__[key]


class Mapper(object):
    def __init__(self, usermapper):
        self.usermapper = usermapper
        self.projections = Config().projections()

    # wrapper around the user's mapper.
    def __call__(self, key, value):
        # from the usermapper: a timestamp, a point in n-space, units and their values.
        for (ts, point, units) in self.usermapper(key, value):
            for pjs in self.projections.values():
                # we perform dimensionality reduction,
                reduced = {}
                for d in pjs:
                    reduced[d] = point[d]
                # yielding for each requested projection.
                for u in units:
                    value = units[u]
                    yield (ts, reduced, u), value

class Reducer(object):
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


# reads conf, creates table.
class Setup(object):
    def go(self):
        c = Config()
        project = c.config['project_name']

        cfs = []
        for p in c.config['projections']:
            projection = '-'.join(c.config['projections'][p])
            cfs.append(projection)

        print "creating table:"
        print "  * " + project
        print " column families:"
        print "".join((map( lambda cf: "  * "+str(cf)+"\n" , cfs)))
        print

        c = setup_transport("localhost")
        create_or_bust(c,project, cfs)


class Import(object):
    def go(self, mapper, input, for_dumbo):

        table = Config().project_name()
        resolver = 'fm.last.darling.HBaseIdentifierResolver'
        outputformat = 'org.apache.hadoop.hbase.mapred.TableOutputFormat'

        opts = [('jobconf',"hbase.mapred.outputtable=" + table),
                ('jobconf','stream.io.identifier.resolver.class=' + resolver),
                ('streamoutput','hbase'), # resolved by identifier.resolver
                ('outputformat', outputformat),
                ('input', input),
                ('output','/tmp/does-not-matter'),
                ('file','lib/utils.py'),
                ('file','lib/zohmg.py'),
                ('file','lib/usermapper.py'),
                ('file','config.yaml')
                ]

        # read class path, attach.
        cp = os.getenv("CLASSPATH")
        for jar in cp.split(':'):
            opts.append(('file', jar))

        # stringify arguments.
        opts_args = ' '.join("-%s '%s'" % (k, v) for (k, v) in opts)
        more_args = ' '.join(for_dumbo)
        dumboargs = "%s %s" % (opts_args, more_args)
        print "giving dumbo these args: " + dumboargs

        # link-magic for usermapper.
        usermapper = os.path.abspath(".")+"/lib/usermapper.py"
        if os.path.isfile(usermapper):
            # TODO: need to be *very* certain we're not unlinking the wrong file.
            os.unlink(usermapper)
        os.symlink(mapper,usermapper)

        # dispatch.
        # TODO: is this where we will source config/env.sh, then?
        os.system("dumbo start tmp/import.py " + dumboargs)


class Serve(object):
    def __init__(self, port=8086, host = 'localhost'):
        import zohmgapp
        from paste import httpserver

        c = Config()
        print "[%s] dataset: %s." % (time.asctime(), c.project_name())

        zapp = zohmgapp.zohmg(c.project_name())
        httpserver.serve(zapp.app, host=host, port=port)
