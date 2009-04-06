# zohmgapp.

import simplejson as json
from paste.request import parse_formvars

from HBaseScanner import HBaseScanner


class zohmg:
    def __init__(self, table):
        self.table = table
        # TODO: read configuration.
        
    # fetches data from hbase,
    # returns dictionary suitable for json dumping.
    def export(self, t0, t1, unit, d0dim, d0val, filters={}):
        print "t0: " + t0
        print "t1: " + t1
        print "unit: " + unit
        print "d0: " + d0dim
        print "d0v: "+ str(d0val)
        print "filters: " + str(filters)
        print ""

        startrow = unit +"-"+ t0
        stoprow  = unit +"-"+ t1 + "~"

        if d0val == "":
            columns = [d0dim+":"]
        else:
            columns = []
            for q in d0val: columns.append(d0dim+":"+q)

            scanner = HBaseScanner.HBaseScanner()
            scanner.connect()
            scanner.open("webmetrics", columns, startrow, stoprow)

            data = {}
            while scanner.has_next():
                r = scanner.next()
                ymd = r.row[-8:]
                t = {}
                for column in r.columns:
                    cf, q = column.split(':')
                    t[q] = r.columns[column].value
                    data[ymd] = t

        # return a list of dicts sorted by ymd
        return [ {k:data[k]} for k in sorted(data) ]


    # strips whitespace
    def strip(self, str):
        return str.strip()

    def app(self, environ, start_response):
        # check input.
        params = parse_formvars(environ)
        try:
            t0 = params['t0']
            t1 = params['t1']
            unit = params['unit']
            d0 = params['d0']
            d0v = map(self.strip, params['d0v'].split(','))
        except:
            start_response('402 PAYMENT REQUIRED', [('content-type', 'text/html')])
            return "missing arguments."

        # TODO: filters.
        filters = {}

        # fetch data.
        data = self.export(t0, t1, unit, d0, d0v, filters)

        # serve output.
        start_response('200 OK', [('content-type', 'text/html')])
        return json.dumps(data)
