# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import simplejson as json
from zohmg.utils import compare_triples, strip
from zohmg.scanner import HBaseScanner


def query(table, projections, params):

    # jsonp.
    try:    jsonp_method = params["jsonp"]
    except: jsonp_method = None

    data = hbase_get(table, projections, params)
    return dump_jsonp(data, jsonp_method)


# returns jsonp which can be used in clients.
def dump_jsonp(data, jsonp_method=None):
    jsondata = json.dumps(data)

    if jsonp_method:
        # client requested data to be wrapped in a function call.
        return jsonp_method + "(" + jsondata + ")"
    else:
        return jsondata


# dimensions is a list of dimensions: ['country', 'usertype', 'useragent']
# values is a dictionary of lists, describing the possible values for each dimension,
# like so: {'country': ['SE', 'DE', 'IT'], 'useragent': ['*'], 'usertype': ['anon']}
#
# returns a list of list of strings that describe the column qualifiers to fetch.
def enumerate_cells(dimensions, values, target=[]):
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

    return enumerate_cells(dimensions[1:], values, newtarget)


# fetches data from hbase,
# returns sorted list of dictionaries suitable for json dumping.
def hbase_get(table, projections, params):
    try:
        t0 = params['t0']
        t1 = params['t1']
        unit = params['unit']
        d0 = params['d0']
        d0v = map(strip, params['d0v'].split(','))
    except:
        raise ValueError

    filters = {}
    # TODO: there must be a neater way of doing this.
    for n in range(1,5):
        try:
            dim = params["d"+str(n)]
            val = params["d"+str(n)+"v"]
            filters[dim] = val
        except:
            continue


    print ""
    print "--- hbase_get ---"
    print "t0: " + t0
    print "t1: " + t1
    print "unit: " + unit
    print "d0: " + d0
    print "d0v: "+ str(d0v)
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
    wanted = set([d0] + filters.keys())
    for p in projections:
        if set(p).issuperset(wanted):
            ps.append((len(p), p.index(d0), p))
    # sort by length, then index; pick the first one.
    pick = sorted(ps, compare_triples)[0][2]
    cf = '-'.join(pick)
    idx = pick.index(d0) # used for dimension-squeezing a bit later.
    print "cf picked: " + cf

    # loop over every dimension in the target column-family
    # and specify value(s) for them.
    qs = {}
    for d in pick:
        if d == d0:
            if d0v == ['']:
                qs[d] = ['.*']
            else:
                qs[d] = d0v
        elif d in filters.keys():
            qs[d] = filters[d]
        else:
            qs[d] = ['all']

    print "qs: " + str(qs)

    # make a list of cells we wish to extract from hbase.
    cells = map(lambda q: cf+":"+q,  map(lambda l: '-'.join(l), enumerate_cells(pick, qs)))
    print "cells: " + str(cells)

    # connect to hbase.
    scanner = HBaseScanner()
    scanner.connect()
    scanner.open(table, cells, startrow, stoprow)

    data = {}
    while scanner.has_next():
        t = {}
        r = scanner.next()
        ymd = r.row[-8:] # extract date from row key.
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
