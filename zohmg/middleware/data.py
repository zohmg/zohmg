import os, sys, time
import simplejson as json
from zohmg.config import Config

# add middleware dir and import data_utils.
sys.path.append(os.path.dirname(__file__))
import data_utils


class data(object):
    def __init__(self):
        self.config = Config()
        self.table = self.config.dataset()
        self.projections = self.config.projections()

    # example query:
    # ?t0=20090120&t1=20090121&unit=pageviews&d0=country&d0v=US,DE
    def __call__(self, environ, start_response):
        print "[%s] Data, serving from table: %s." % (time.asctime(),self.table)

        # fetch data.
        start = time.time()
        try: data = data_utils.hbase_get(self.table,self.projections,environ) # query is in environ.
        except ValueError:
            print >>sys.stderr, "Error: Could not parse query."
        elapsed = (time.time() - start)
        sys.stderr.write("hbase query+prep time: %s\n" % elapsed)

        # serve output.
        start_response('200 OK', [('content-type', 'text/html')])
        return "jsonZohmgFeed(" + json.dumps(data) + ")" # jsonp.
