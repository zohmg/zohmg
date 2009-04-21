from zohmg.config import Config, Environ
import os

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

        cp = env.get("CLASSPATH")
        if cp is not None:
            for jar in cp.split(':'):
                opts.append(('file', jar))
        else:
            msg = "E: CLASSPATH in config/environment is empty."
            fail(msg)


        # pull everything in config and lib.
        # TODO
        print os.walk("lib")
        print os.walk("config")

        # stringify arguments.
        opts_args = ' '.join("-%s '%s'" % (k, v) for (k, v) in opts)
        more_args = ' '.join(for_dumbo) # TODO: is this necessary?
        dumboargs = "%s %s" % (opts_args, more_args)
        print "giving dumbo these args: " + dumboargs

        # link-magic for usermapper.
        usermapper = os.path.abspath(".")+"/lib/usermapper.py"
        if os.path.isfile(usermapper):
            # SECURITY
            # TODO: need to be *very* certain we're not unlinking the wrong file.
            os.unlink(usermapper)
        os.symlink(mapper,usermapper)

        # dispatch.
        os.system("dumbo start tmp/import.py " + dumboargs)
