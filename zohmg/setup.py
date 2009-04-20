from zohmg.config import Config
from utils import *

# reads conf, creates table.
class Setup(object):
    def go(self):
        c = Config()
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

        c = setup_transport("localhost")
        create_or_bust(c,project, cfs)
