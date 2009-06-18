#!/usr/bin/env python
# these here programming codes are licensed under the gnu fearsome dude license.

from random import random

from hbase import Hbase
from hbase.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

def setup_thrift_transport(host):
  transport = TSocket.TSocket(host, 9090)
  transport = TTransport.TBufferedTransport(transport)
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = Hbase.Client(protocol)
  transport.open()
  return client, transport


table = 'submissions-test'

units = ['scrobbles', 'loves']
scaling = {'scrobbles': 100, 'loves': 2}

dimensions  = ['user', 'artist', 'track', 'album']
projections = [('user'), ('artist', 'track'), ('user','artist','track','album')]

year="2009"
months = range(0, 12)
days   = range(0, 30)


# possible attribute values.
attrs = {'users':   [120, 240, 360],
         'artists': [1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
         'track':   range(0,512),
         'album':   range(0,64)}



def random_attribute_of(dimension):
    try:
        possible = attrs[dimension]
    except:
        print 'oh noes.'
        return '0.'
    r = int(random(len(possible)))
    attr = possible[r]
    return attr
        

def magic_precomputation():
    # so as to not make the distribution entirely random.
    hashes = {}
    for dimension in attrs.keys():
        hashes[dimension] = {}
        for attr in attrs[dimension]:
            hashes[dimension][attr] = hash(attr) % 255
    return hashes

def magic_computation(unit, dimension):
    return random() * hashes[dimension] * scaling[unit]

def generate_data(client):
    for month in months:
        month = "%02d" % (month+1)
        for day in days:
            ymd = year + month + "%02d" % day
            for projection in projections:
                rowkeyarray = []
                for dimension in projection:
                    rowkeyarray.append(dimension)
                    rowkeyarray.append(random_attribute_of(dimension)) # random.
                    rowkeyarray.append(ymd)
                    rowkey = '-'.join(rowkeyarray)
                    print 'rocknroll, know what im sayin: ' + rowkey

                    mutations = []
                    for unit in units:
                        m = {}
                        m['column'] = "unit:" + unit
                        m['value']  = str(int(magic_computation(unit, dimension)))
                        mutations.append(Mutation(m))
                    print rowkey + " +> " + str(len(mutations)) + " mutations."
                    #client.mutateRow(table, rowkey, mutations)


if __name__ == '__main__':
    client, transport = setup_thrift_transport('localhost')

    hashes = magic_precomputation()
    generate_data(client)

    transport.close()
