# zohmgapp.

import simplejson as json
from paste.request import parse_formvars

from HBaseScanner import HBaseScanner
from zohmg import Config

class zohmg:
    def __init__(self, table):
        self.config = Config()
        self.table = self.config.project_name()
        self.projections = self.config.projections()
        
    # fetches data from hbase,
    # returns sorted list of dictionaries suitable for json dumping.
    def export(self, t0, t1, unit, d0dim, d0val, filters={}):
        print "--- export ---"
        print "t0: " + t0
        print "t1: " + t1
        print "unit: " + unit
        print "d0: " + d0dim
        print "d0v: "+ str(d0val)
        print "filters: " + str(filters)
        print "--------------"

        startrow = unit +"-"+ t0
        stoprow  = unit +"-"+ t1 + "~"

        # massage the filters.
        # 'all' or '*' means we take away the dimension from the filter list.
        for k in filters.copy():
            if filters[k] in ['all', '*']:
                del filters[k]
            else:
                filters[k] = filters[k].split(',') # make into list.

        # pick the best-suiting projection p.
        # 1) p must contain all dimensions we specify.
        # 2) of all ps satisfying 1, the position of d0 in p must be leftmost,
        #    and p must be the shortest of the fitting candidates.
        ps = [] # projection candidates.
        wanted = set([d0dim] + filters.keys())
        for p in self.projections.values():
            if set(p).issuperset(wanted):
                ps.append((len(p), p.index(d0dim), p))
        # sort by length, then index; pick the first one.
        pick = sorted(ps, self.compare_tuples)[0][2]
        cf = '-'.join(pick)
        print "cf picked: " + cf

        # loop over every dimension in the target column-family
        # and specify value(s) for them.
        qs = {}
        for d in pick:
            if d == d0dim:
                if d0val == ['']:
                    qs[d] = ['.*']
                else:
                    qs[d] = d0val
            elif d in filters.keys():
                qs[d] = filters[d]
            else:
                qs[d] = 'all'

        print "qs: " + str(qs)
        
        # let's go recursive.
        cells = map(lambda q: cf+":"+q,  map(lambda l: '-'.join(l), self.enumerate_cells(pick, qs)))

        print "cells: " + str(cells)

        scanner = HBaseScanner.HBaseScanner()
        scanner.connect()
        scanner.open(self.table, cells, startrow, stoprow)

        # we're getting columns back,
        # and now we need to squeeze all values into a single dimension again. ah!
        idx = pick.index(d0dim)

        data = {}
        while scanner.has_next():
            r = scanner.next()
            ymd = r.row[-8:]
            t = {} # target.
            for column in r.columns:
                cf, q = column.split(':')
                dimensions = q.split('-')
                d = dimensions[idx]
                t[d] = t.get(d, 0)
                t[d] += int(r.columns[column].value)
                data[ymd] = t


        # returns a list of dicts sorted by ymd.
        return [ {k:data[k]} for k in sorted(data) ]

    # strips whitespace
    def strip(self, str):
        return str.strip()

    # dimensions is a list of dimensions: ['country', 'usertype', 'useragent']
    # values is a dictionary of lists, describing the possible values for each dimension,
    # like so: {'country': ['SE', 'DE', 'IT'], 'useragent': ['*'], 'usertype': ['anon']}
    #
    # returns a list of list of strings that describe the column qualifiers to fetch.
    def enumerate_cells(self, dimensions, values, target=[]):
        if dimensions == []:
            # base case.
            return target

        newtarget = []
        if target == []:
            # first time around.
            for value in values[dimensions[0]]:
                newtarget.append([value])
        else:
            for t in target:
                for value in values[dimensions[0]]:
                    newtarget.append(t + [value])

        return self.enumerate_cells(dimensions[1:], values, newtarget)

    # x and y are three-tuples, like so: (4, 2, [..])
    # we sort by first element, then by the second one.
    def compare_tuples(self, x, y):
        a,b,c = x
        d,e,f = y
        if a < d: return -1
        if a > d: return 1
        if b < e: return -1
        if b > e: return 1
        return 0


    # entry-point of service.
    def app(self, environ, start_response):

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

        filters = {}
        for n in range(1,5):
            try:
                dim = params["d"+str(n)]
                val = params["d"+str(n)+"v"]
                filters[dim] = val
            except:
                continue

        # fetch data.
        data = self.export(t0, t1, unit, d0, d0v, filters)

        # serve output.
        start_response('200 OK', [('content-type', 'text/html')])
        return json.dumps(data)
