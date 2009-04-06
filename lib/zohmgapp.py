# zohmgapp.

import simplejson as json
from paste.request import parse_querystring
from paste.request import parse_formvars

from HBaseScanner import HBaseScanner


# fetches data from hbase,
# returns dictionary suitable for json dumping.
def export(t0, t1, unit, d0, filters={}):
    print "t0: " + t0
    print "t1: " + t1
    print "unit: " + unit
    print "d0: " + d0[0]
    print "d0v: "+ str(d0[1])
    print "filters: " + str(filters)
    print ""

    startrow = unit +"-"+ t0
    stoprow  = unit +"-"+ t1 + "~"


    scanner = HBaseScanner.HBaseScanner()
    scanner.connect()
    scanner.open("webmetrics", ["country:SE", "country:DE", "country:US"], startrow, stoprow)

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



def app(environ, start_response):
    params = parse_formvars(environ)

    t0 = params['t0']
    t1 = params['t1']
    unit = params['unit']
    d0 = params['d0']
    d0v = params['d0v'].split(',')

    if t0=="" or t1=="" or d0=="":
        start_response('402 PAYMENT REQUIRED', [('content-type', 'text/html')])
        return "missing arguments."

    filters = {}

    # data.
    #data = [{'20090101':{'cherry':512}, '20090102':{'cherry':1024}, '20090103':{'cherry':600}}]
    data = export(t0, t1, unit, (d0,d0v), filters)


    start_response('200 OK', [('content-type', 'text/html')])
    return json.dumps(data)
