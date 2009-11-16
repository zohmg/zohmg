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

# this is the command line interface.

import sys, os, getopt
from zohmg.utils import fail

# add all bundled eggs to sys.path
eggpath='/usr/local/lib/zohmg/egg'
for (dir, dirnames, files) in os.walk(eggpath):
    for file in files:
        suffix = file.split(".")[-1]
        if suffix == "egg":
            sys.path.append(dir+"/"+file)

# TODO: read version from $somewhere.
version = '0.2.3-dev'

def usage(reason = None):
    zohmg = os.path.basename(sys.argv[0])
    if reason:
        print "error: " + reason
    print "zohmg " + version
    print "usage:"
    print zohmg + " create <dir>"
    print zohmg + " setup"
    print zohmg + " import <mapper> <input-dir> [--local] [--lzo]"
    print zohmg + " server [--host=<host>] [--port=<port>]"
    print zohmg + " reset"
    print zohmg + " help"

def print_version():
    print "zohmg version " + version

def print_help():
    print "Need help?"
    print
    print "There are a few documents in /usr/local/share/zohmg/doc that might be of some help,"
    print "and there's an IRC channel -- #zohmg on freenode -- where you can ask questions."


# command line entry-point.
def zohmg():
    try:
        # read the first argument.
        cmd = sys.argv[1]
    except:
        # there was no first argument.
        usage()
        sys.exit(0)

    if   cmd == 'create' : create()
    elif cmd == 'setup'  : setup()
    elif cmd == 'import' : process()
    elif cmd == 'server' : server()
    elif cmd == 'reset'  : reset()
    elif cmd in ['version', '--version']: print_version()
    elif cmd in ['help',    '--help']:    print_help()
    else: usage()

def create():
    from zohmg.create import Create
    try:
        path = sys.argv[2]
    except:
        usage("create needs an argument.")
        sys.exit(1)

    Create(path)


def setup():
    refuse_to_act_in_nonzohmg_directory()
    from zohmg.setup import Setup
    Setup().go()

# import.
def process():
    refuse_to_act_in_nonzohmg_directory()
    from zohmg.process import Process
    try:
        # check for two arguments,
        mapper = sys.argv[2]
        # (works only with relative paths for now.)
        mapperpath = os.path.abspath(".")+"/"+mapper
        inputdir = sys.argv[3]
        dumbo_args = sys.argv[4:]
    except:
        usage("import needs two arguments.")
        sys.exit(1)

    Process().go(mapperpath, inputdir, dumbo_args)


def server():
    refuse_to_act_in_nonzohmg_directory()
    import zohmg.server
    host, port = zohmg.server.defaults()

    try:
        opts, args = getopt.getopt(sys.argv[2:], "h:p:", ["host=", "port="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    
    for o, a in opts:
        if o in ("-h", "--host"):
            host=a
        elif o in ("-p", "--port"):
            port=a
        else:
            assert False, "unhandled option"

    project_dir = os.path.abspath("")
    zohmg.server.start(project_dir, host=host, port=port)


def reset():
    refuse_to_act_in_nonzohmg_directory()
    from zohmg.reset import Reset
    Reset().please()


# exits if 'zohmg' was run in a directory without the special .zohmg-file.
def refuse_to_act_in_nonzohmg_directory():
    cwd = os.getcwd()
    if not os.path.exists(cwd+"/.zohmg"):
        msg = "error: This is not a proper zohmg project."
        fail(msg)
