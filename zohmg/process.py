from zohmg.config import Config, Environ
import os, re

class Process(object):
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
                # Push zohmg egg.
                ('libegg','/usr/lib/python2.5/site-packages/zohmg-0.0.1-py2.5.egg'),
                ]

        # read environment and attach.
        env = Environ()

        opts.append(('hadoop',env.get("HADOOP_HOME")))

        classpath = env.get("CLASSPATH")
        if classpath is not None:
            for jar in classpath:
                opts.append(('file', jar))
        else:
            msg = "E: CLASSPATH in config/environment is empty."
            fail(msg)

        # pull everything in config and lib.
        # XXX: assuming we only have one directory level here.
        # ignore .pyc files.
        for entry in os.walk("lib"):
            dir,dirnames,files = entry
            opts.extend([('file','lib/'+f) for f in files if not f[-4:] == ".pyc"])

        for entry in os.walk("config"):
            dir,dirnames,files = entry
            opts.extend([('file','config/'+f) for f in files if not f[-4:] == ".pyc"])

        # stringify arguments.
        opts_args = ' '.join("-%s '%s'" % (k, v) for (k, v) in opts)
        more_args = ' '.join(for_dumbo) # TODO: is this necessary?
        dumboargs = "%s %s" % (opts_args, more_args)
        print "giving dumbo these args: " + dumboargs

        # link-magic for usermapper.
        usermapper = os.path.abspath(".")+"/lib/usermapper.py"
        if os.path.isfile(usermapper):
            # TODO: need to be *very* certain we're not unlinking the wrong file.
            os.unlink(usermapper)
        # TODO: SECURITY, need to be certain that we symlink correct file.
        os.symlink(mapper,usermapper)

        # dispatch.
        os.system("dumbo start /usr/local/lib/zohmg/import.py " + dumboargs)
