#!/usr/bin/env python

# usage:
#  $> zohmg setup
#  $> zohmg import mapper.py hdfs-input-dir
#  $> zohmg serve [--port <port>]

import sys, os

def usage(reason=None):
    if reason:
        print "error: " + reason
    print "usage:"
    print " %s setup" % sys.argv[0]
    print " %s import <mapper> <hdfs-input-dir>" % sys.argv[0]
    print " %s serve [--port <port>]" % sys.argv[0]


# read arguments.
try:
    cmd=sys.argv[1]
except:
    usage()
    sys.exit(1)


if cmd == "setup":
    from zohmg import Setup
    Setup().go()
elif cmd == 'import':
    # check for two arguments,
    try:
        mapper = sys.argv[2]
        # works only with relative paths for now.
        mapperpath = os.path.abspath(".")+"/"+mapper
        inputdir = sys.argv[3]
        dumbo_args = sys.argv[4:]
    except:
        usage("import needs three arguments.")
        sys.exit(1)
    from zohmg import Import
    Import().go(mapperpath, inputdir, dumbo_args)
elif cmd == 'serve':
    # check for optional argument.
    try:    port = sys.argv[2]
    except: port = 8086 # that's ok.
    from zohmg import Serve
    Serve.serve(port)
else:
    usage()
