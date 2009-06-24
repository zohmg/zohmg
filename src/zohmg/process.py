# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from zohmg.config import Config, Environ
from zohmg.utils import fail
import sys, os, re

class Process(object):
    def go(self, mapper, input, for_dumbo):
        local_mode = False # default: run jobs on Hadoop.
        local_output_path = '/tmp/zohmg-output' # TODO: make user configurable.

        table = Config().dataset()
        jobname = "%s %s" % (table, input) # overrides any name specified on cli.

        resolver = 'fm.last.darling.hbase.HBaseIdentifierResolver'
        outputformat = 'org.apache.hadoop.hbase.mapreduce.TableOutputFormat'

        opts = [('jobconf', "hbase.mapred.outputtable=" + table),
                ('jobconf', 'stream.io.identifier.resolver.class=' + resolver),
                ('streamoutput', 'hbase'), # resolved by identifier.resolver
                ('outputformat', outputformat),
                ('input', input),
                ('file', 'lib/usermapper.py'), # TODO: handle this more betterer.
                ('name', jobname)
               ]

        # add zohmg-*.egg
        zohmg_egg = [z for z in sys.path if "zohmg" in z][0]
        opts.append(('libegg', zohmg_egg))

        # add files to the jobjar from these paths
        jar_path = '/usr/local/lib/zohmg/jar'
        egg_path = '/usr/local/lib/zohmg/egg'
        directories = ["config", "lib", jar_path, egg_path]
        file_opts = self.__add_files(directories)
        opts.extend(file_opts)

        ## check extra arguments.
        # TODO: allow for any order of extra elements.
        #       as it stands, --local must be specified before --lzo.
        # first, check for '--local'
        if len(for_dumbo) > 0 and for_dumbo[0] == '--local':
            local_mode = True
            for_dumbo.pop(0) # remove '--local'.
        # check for '--lzo' as first extra argument.
        if len(for_dumbo) > 0 and for_dumbo[0] == '--lzo':
            print 'lzo mode: enabled.'
            opts.append(('inputformat', 'org.apache.hadoop.mapred.LzoTextInputFormat'))
            for_dumbo.pop(0) # remove '--lzo'.

        env = Environ()

        if local_mode:
            print 'local mode: enabled.'
            opts.append(('output', local_output_path))
        else:
            print 'hadoop mode: enabled.'
            hadoop_home = env.get("HADOOP_HOME")
            if not os.path.isdir(hadoop_home):
                msg = "error: HADOOP_HOME in config/environment.py is not a directory."
                fail(msg)
            opts.append(('output', '/tmp/does-not-matter'))
            opts.append(('hadoop', hadoop_home))

        # add jars defined in config/environment.py to jobjar.
        classpath = env.get("CLASSPATH")
        if classpath is not None:
            for jar in classpath:
                if not os.path.isfile(jar):
                    msg = "error: jar defined in config/environment is not a file: %s." % jar
                    fail(msg)
                else:
                    print 'import: adding %s to jobar.' % jar
                    opts.append(('libjar', jar))
        else:
            msg = "error: CLASSPATH in config/environment is empty."
            fail(msg)

        # stringify arguments.
        opts_args = ' '.join("-%s '%s'" % (k, v) for (k, v) in opts)
        more_args = ' '.join(for_dumbo) # TODO: is this necessary?
        dumboargs = "%s %s" % (opts_args, more_args)
        print "giving dumbo these args: " + dumboargs

        # link-magic for usermapper.
        usermapper = os.path.abspath(".") + "/lib/usermapper.py"
        if os.path.isfile(usermapper):
            # TODO: need to be *very* certain we're not unlinking the wrong file.
            os.unlink(usermapper)
        # TODO: SECURITY, need to be certain that we symlink correct file.
        # TODO: borks if lib directory does not exist.
        os.symlink(mapper, usermapper)

        # let the user know what will happen.
        if local_mode:
            print 'doing local run.'
            print 'data will not be imported to hbase.'
            print 'output is at ' + local_output_path

        # dispatch.
        # PYTHONPATH is added because dumbo makes a local run before
        # engaging with hadoop.
        os.system("PYTHONPATH=lib dumbo start /usr/local/lib/zohmg/mapred/import.py " + dumboargs)


    # reads directories and returns list of tuples of
    # file/libegg/libjar options for dumbo.
    def __add_files(self,dirs):
        opts = []
        # TODO: optimize? this is now O(dirs*entries*files).
        for dir in dirs:
            for entry in os.walk(dir):
                dir,dirnames,files = entry
                # for each file add it with correct option.
                for file in files:
                    if not os.path.isfile(dir+"/"+file):
                        msg = "error: File not found, %s." % file
                        fail(msg)

                    suffix = file.split(".")[-1]
                    option = None
                    if   suffix == "egg":  option = "libegg"
                    elif suffix == "jar":  option = "libjar"
                    elif suffix == "py":   option = "file"
                    elif suffix == "yaml": option = "file"

                    if option:
                        print 'import: adding %s to jobjar.' % file
                        opts.append((option, dir+"/"+file))
                    else:
                        print "import: ignoring " + dir+'/'+file
        return opts
