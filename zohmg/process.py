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
                # Push zohmg egg and darling jar.
                ('libegg','/usr/lib/python2.5/site-packages/zohmg-0.0.1-py2.5.egg'),
                ('libjar','/usr/local/lib/zohmg/darling-0.0.3.jar')
               ]

        # read environment and attach.
        env = Environ()

        opts.append(('hadoop',env.get("HADOOP_HOME")))

        classpath = env.get("CLASSPATH")
        if classpath is not None:
            for jar in classpath:
                opts.append(('libjar', jar))
        else:
            msg = "E: CLASSPATH in config/environment is empty."
            fail(msg)

        # pull everything in config and lib.
        file_opts = self.__add_files(["config","lib"])
        opts.extend(file_opts)

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
        # PYTHONPATH is added because dumbo makes a local run before
        # engaging with hadoop.
        os.system("PYTHONPATH=lib; dumbo start /usr/local/lib/zohmg/import.py " + dumboargs)


    # reads directories and returns list of tuples of
    # file/libegg/libjar options for dumbo.
    def __add_files(self,dirs):
        opts = []
        # TODO: optimize. this is now O(n^3).
        for dir in dirs:
            for entry in os.walk(dir):
                dir,dirnames,files = entry
                # for each file add it with correct option.
                for file in files:
                    option = None
                    suffix = file.split(".")[-1] # infer file suffix.

                    # ignore all other files but egg/jar/yaml.
                    if   suffix == "egg":  option = "libegg"
                    elif suffix == "jar":  option = "libjar"
                    elif suffix == "yaml": option = "file"
                    #elif suffix == "py":   option = "pyfile" # TODO: implement this in dumbo maybe?
                    # TODO: what about text files or other files the user wants?
                    #       we still want to ignore certain files (e.g. .pyc).

                    if option:
                        opts.append((option,file))

        return opts
