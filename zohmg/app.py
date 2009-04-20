# zohmgapp.

# paste-compatible application for serving.. yes, what exactly?
# zohmg.app() is the entry-point. begin your code-reading journey there.

import sys, time
import simplejson as json
from paste.request import parse_formvars

from HBaseScanner import HBaseScanner
from zohmg.config import Config

class App(object):
    def __init__(self, table):
        self.config = Config()
        self.table = self.config.project_name()
        self.projections = self.config.projections()

    # fetches data from hbase,
    # returns sorted list of dictionaries suitable for json dumping.
    def export(self, t0, t1, unit, d0dim, d0val, filters={}):
        print ""
        print "--- export ---"
        print "t0: " + t0
        print "t1: " + t1
        print "unit: " + unit
        print "d0: " + d0dim
        print "d0v: "+ str(d0val)
        print "filters: " + str(filters)
        print "--------------"

        # the row key is 'unit-ymd', i.e. "pageviews-20090410". 
        startrow = unit +"-"+ t0
        stoprow  = unit +"-"+ t1 + "~"

        # massage the filters.
        for k in filters.copy():
            if filters[k] in ['all', '*']:
                # 'all' or '*' is equivalent to not filtering at all.
                del filters[k]
            else:
                # turn it into a list.
                filters[k] = filters[k].split(',')

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
        idx = pick.index(d0dim) # used for dimension-squeezing a bit later.
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
                qs[d] = ['all']

        print "qs: " + str(qs)

        # make a list of cells we wish to extract from hbase.
        cells = map(lambda q: cf+":"+q,  map(lambda l: '-'.join(l), self.enumerate_cells(pick, qs)))
        print "cells: " + str(cells)

        # connect to hbase.
        scanner = HBaseScanner.HBaseScanner()
        scanner.connect()
        scanner.open(self.table, cells, startrow, stoprow)

        data = {}
        while scanner.has_next():
            t = {}
            r = scanner.next()
            # extract date from row key.
            ymd = r.row[-8:]
            for column in r.columns:
                # split,
                cf, q = column.split(':')
                dimensions = q.split('-')
                # squash,
                d = dimensions[idx]
                t[d] = t.get(d, 0)
                t[d] += int(r.columns[column].value)
                # and save.
                data[ymd] = t

        # returns a list of dicts sorted by ymd.
        return [ {ymd:data[ymd]} for ymd in sorted(data) ]

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
    # return 1, 0, or -1 if x is larger than, equal to, or less than y.
    def compare_tuples(self, x, y):
        a,b,c = x
        d,e,f = y
        if a > d: return 1
        if a < d: return -1
        if b > e: return 1
        if b < e: return -1
        return 0


    # entry-point of service.

    # example query:
    # ?t0=20090120&t1=20090121&unit=pageviews&d0=country&d0v=US,DE
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
            return "you might be looking for the helpful <a href='http://localhost/:8080/'>user interface</a>."

        filters = {}
        # TODO: there must be a neater way of doing this.
        for n in range(1,5):
            try:
                dim = params["d"+str(n)]
                val = params["d"+str(n)+"v"]
                filters[dim] = val
            except:
                continue

        # fetch data.
        start = time.time()
        data = self.export(t0, t1, unit, d0, d0v, filters)
        elapsed = (time.time() - start)
        sys.stderr.write("hbase query+prep time: %s\n" % elapsed)

        # serve output.
        start_response('200 OK', [('content-type', 'text/html')])
        return "jsonZohmgFeed(" + json.dumps(data) + ")" # jsonp.
