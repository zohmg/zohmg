#!/usr/bin/python
from random import random
from hbase.ttypes import *


def setup_transport(host):
  from thrift import Thrift
  from thrift.transport import TSocket
  from thrift.transport import TTransport
  from thrift.protocol import TBinaryProtocol
  from hbase import Hbase
  transport = TSocket.TSocket(host, 9090)
  transport = TTransport.TBufferedTransport(transport)
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = Hbase.Client(protocol)
  transport.open()
  return client


# set up some test data. should be quick.

table = 'webmetrics'

units = ['bytes', 'pageviews']
scaling = {'bytes': 1000, 'pageviews': 5}

countries = ['US', 'SE', 'DE', 'ES', 'GB', 'FR']
hashes = {} # pre-compute country hashes.
for c in countries: hashes[c] = hash(c) % 255

client = setup_transport('localhost')

year="2009"
for month in ['04', '05', '06']:
    for day in range(1,31):
        for unit in units:
            ymd = year + month + "%02d" % day
            rk = unit + "-" + ymd
            mutations = []
            for c in countries:
                m = {}
                m['column'] = "country:"+c
                m['value']  = str(int(random() * hashes[c] * scaling[unit]))
                mutations.append(Mutation(m))
                print rk + " +> " + str(mutations)
            client.mutateRow(table, rk, mutations)
