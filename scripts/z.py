#!/usr/bin/env python

# usage:
#  $> zohmg setup
#  $> zohmg import mapper.py hdfs-input-dir
#  $> zohmg serve [--port <port>]

import sys, os
#sys.path.append(os.path.abspath(".") + "/lib") # FIXME.


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
    #
    try:
        # XXX: only relative for now.
        mapper = os.path.abspath(".")+"/"+sys.argv[2]
        inputdir = sys.argv[3]
        for_dumbo = sys.argv[4:]
    except:
        usage("import needs three arguments.")
        sys.exit(1)
    from zohmg import Import
    Import().go(mapper, inputdir, for_dumbo)
elif cmd == 'serve':
    # check for optional argument.
    try:    port = sys.argv[2]
    except: port = 8086 # that's ok.
    from zohmg import Serve
    serve(port)
else:
    usage()

