#!/usr/bin/env python

# TODO: use this in the other modules.

import sys, os
abspath=os.path.dirname(os.path.abspath(sys.argv[0]))
libpath='/'.join([abspath, "..", "lib"])
sys.path.append(libpath)

print libpath
