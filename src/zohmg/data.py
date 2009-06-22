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

# zohmg.data, hello.

import sys
import simplejson as json

from zohmg.utils import compare_triples, strip
from zohmg.scanner import HBaseScanner


class DataNotFound(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error

class NoSuitableProjection(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error

class MissingArguments(Exception):
    def __init__(self, value):
        self.error = value
    def __str__(self):
        return self.error



# public interface.
def query(table, projections, params):

    # jsonp.
    try:    jsonp_method = params["jsonp"]
    except: jsonp_method = None

    # check parameters.
    querydict = {}
    try:
        querydict['t0'] = params['t0']
        querydict['t1'] = params['t1']
        querydict['d0'] = params['d0']
        querydict['d0v'] = map(strip, params['d0v'].split(',')) # => ['SE', 'DE', 'US']
        querydict['unit'] = params['unit']
    except KeyError, e:
        raise MissingArguments(str(e))

    print ""
    print "-- QUERY --"
    print "t0: " + querydict['t0']
    print "t1: " + querydict['t1']
    print "unit: " + querydict['unit']
    print "d0: " + querydict['d0']
    print "d0v: "+ str(querydict['d0v'])
    print "----------"



    data = hbase_get(table, projections, querydict)
    return dump_jsonp(data, jsonp_method)


# TODO: classify.

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


def find_suitable_projection(projections, d0, filters):
    # pick the best-suiting projection p.
    # 1) p must contain all dimensions we specify.
    # 2) of all ps satisfying 1, the position of d0 in p must be leftmost,
    #    and p must be the shortest of the fitting candidates.

    ps = [] # projection candidates.
    wanted = set([d0] + filters.keys())

    for p in projections:
        if set(p).issuperset(wanted):
            ps.append((len(p), p.index(d0), p))

    if len(ps) == 0: return None # no suitable projections!

    # sort by length, then index; pick the first one.
    projection = sorted(ps, compare_triples)[0][2]
    return projection


# fetches data from hbase,
# returns sorted list of dictionaries suitable for json dumping.
# TODO: private.
def hbase_get(table, projections, query):
# query is guaranteed to have the following keys:
#  t0, t1, unit, d0, d0v


    # TODO: do this in query().
    # TODO: there must be a neater way of doing this.
    filters = {}
    for n in range(1,5):
        try:
            dim = query["d"+str(n)]
            val = query["d"+str(n)+"v"]
            filters[dim] = val
        except:
            continue

    # massage the filters.
    for key in filters.copy():
        if filters[key] in ['all', '*']:
            # 'all' or '*' is equivalent to not filtering at all.
            del filters[key]
        else:
            # turn comma-delimited string into list.
            filters[key] = filters[key].split(',')

    print "filters: " + str(filters)



    projection = find_suitable_projection(projections, query['d0'], filters)
    if projection == None:
        print 'could not find a suitable projection for ' + query['d0']
        raise NoSuitableProjection("could not find a suitable projection for dimension " + query['d0'])
    print "most suited projection: " + str(projection)

    # TODO: ask rowkeyformatter.
    rowkeyarray = []
    for d in projection:
        rowkeyarray.append(d)
        # this becomes a bit tricky..
        if d == query['d0']:
            rowkeyarray.append(query['d0v'][0]) # TODO: fix!
            # TODO?: if d0v = [''], append 'all'
        elif d in filters.keys():
            rowkeyarray.append(filters[d])
        else:
            rowkeyarray.append('all')
    rowkey = '-'.join(rowkeyarray)

    # the row key is 'dimension-value-[dimension-value, ..]-ymd',
    # i.e. 'artist-97930-track-102203-20090601'
    startrow = rowkey + '-' + query['t0']
    stoprow  = rowkey + '-' + query['t1'] + "~"
    
    print "start: " + startrow
    print "stop:  " + stoprow

    # format column-family + qualifier
    cfq = 'unit:' + query['unit']

    # connect to hbase.
    scanner = HBaseScanner()
    scanner.connect()
    scanner.open(table, [cfq], startrow, stoprow)

    data = {}
    d = query['d0'] # TODO: fix.
    numrows = 0
    while True:
        t = {}
        numrows += 1
        next = scanner.next()
        if next == []:
            break
        r = next[0]
        # extract date from row key.
        ymd = r.row[-8:]
        # read possible old values, add.
        for column in r.columns:
            t[d] = t.get(d, 0)
            t[d] += int(r.columns[column].value)
        # and save.
        data[ymd] = t
    print "rows: " + str(numrows)

    # returns a list of dicts sorted by ymd.
    return [ {ymd:data[ymd]} for ymd in sorted(data) ]
