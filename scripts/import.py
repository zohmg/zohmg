#!/usr/bin/env python

import sys, os
import dumbo

# get our reducers, etc.
sys.path.append(os.path.abspath(".") + "/lib") # FIXME.
from reducers import *

# this script is acting as a go-between for 'dumbo start'.


def usage():
    print "usage: " + sys.argv[0] + " <map.py> <dumboesque arguments>"

try:
    #mapper=sys.argv[1]
    pass
except IndexError:
    usage()
    sys.exit(1)

mapper='mappers/m0.py'

# 1) suck in user's map.
sys.path.append(".")
m = __import__(mapper.split(".")[0])
# TODO: make sure module has method 'map'.


# wrap user's mapper.
def mapper_wrapper(m):
    def g(k,v):
        for r in m("yeah-"+str(k), v):
            ts, dims, units = r
            for u in units:
                rk = '-'.join([u, str(ts)])
                yield (rk, dims), units[u]
    return g



# 2) run w/ dumbo
dumbo.run(mapper_wrapper(m.map), reducer)

# 3) ..
# 4) profit.

