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
  return client, transport


# set up some test data. should be quick.

table = 'webmetrics'

units = ['bytes', 'pageviews']
scaling = {'bytes': 1000, 'pageviews': 5}

countries = ['US', 'SE', 'DE', 'ES', 'GB', 'FR', 'IT', 'DK']
hashes = {} # pre-compute country hashes.
for c in countries: hashes[c] = hash(c) % 255

client, transport = setup_transport('localhost')

year="2009"
for month in range(1,13):
    month = "%02d" % month
    for day in range(1,31):
        ymd = year + month + "%02d" % day
        for unit in units:    
            rk = unit + "-" + ymd
            mutations = []
            for c in countries:
                m = {}
                m['column'] = "country:"+c
                m['value']  = str(int(random() * hashes[c] * scaling[unit]))
                mutations.append(Mutation(m))
            print rk + " +> " + str(len(mutations)) + " mutations."
            client.mutateRow(table, rk, mutations)

transport.close()
