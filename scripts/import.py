#!/usr/bin/env python

import sys, os
import dumbo

# get our reducers, etc.
sys.path.append(os.path.abspath(".") + "/lib") # FIXME.
from reducers import *


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





# 2) run w/ dumbo
dumbo.run(mapper_wrapper(m.map), reducer)

# 3) ..
# 4) profit.

