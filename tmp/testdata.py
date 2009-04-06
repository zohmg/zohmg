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
countries = ['US', 'SE', 'DE']
client = setup_transport('localhost')

year="2009"
for month in ['01', '02', '03']:
    for day in range(1,31):
        ymd = year + month + "%02d" % day
        rk = "pageviews-" + ymd
        mutations = []
        for c in countries:
            m = {}
            m['column'] = "country:"+c
            m['value']  = str(int(random() * 255))
            mutations.append(Mutation(m))
        client.mutateRow(table, rk, mutations)
