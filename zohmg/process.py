from zohmg.config import Config
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
                ('file','lib/utils.py'),
                ('file','lib/zohmg.py'),
                ('file','lib/usermapper.py'),
                ('file','config.yaml')
                ]

        # read class path, attach.
        cp = os.getenv("CLASSPATH")
        if cp != None:
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
