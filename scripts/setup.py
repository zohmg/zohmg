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
for p in c.config['projections']:
    projection = '-'.join(c.config['projections'][p])
    cfs.append(projection)

print "creating table:" 
print "  * " + project
print " column families:"
print "".join((map( lambda cf: "  * "+str(cf)+"\n" , cfs)))
print

c = setup_transport('localhost')
create_or_bust(c, project, cfs)
