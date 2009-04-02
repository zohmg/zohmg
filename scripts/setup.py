#!/usr/bin/python

# reads conf, creates table.
import os, sys
sys.path.append(os.path.abspath(".") + "/lib") # FIXME.

from read_config import *
from utils import *

c = config()
c.read_config()

project = c.config['project_name']
cfs = []
for unit in c.config['units']:
    for p in c.config['units'][unit]:
        projection = '-'.join(c.config['units'][unit][p])
        # TODO: urlencode projection.
        print projection
        cfs.append(projection)

print "creating tables for " + project + " with these column families: " + str(cfs )

c = setup_transport('localhost')
create_or_bust(c, project, cfs)
