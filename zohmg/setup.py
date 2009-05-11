from zohmg.config import Config
from utils import *

# reads conf, creates table.
class Setup(object):
    def go(self):
        c = Config()
        dataset = c.config['dataset']

        cfs = []
        for p in c.config['projections']:
            projection = '-'.join(c.config['projections'][p])
            cfs.append(projection)

        print "creating table '%s'" % dataset
        print " column families:"
        print "".join((map( lambda cf: "  + "+str(cf)+":\n" , cfs)))

        try:
            c = setup_transport("localhost")
        except:
            sys.stderr.write("could not setup thrift transport.\n")
            sys.stderr.write("is the thrift server turned on?\n")
            sys.exit(1)

        create_or_bust(c, dataset, cfs)
