#!/usr/bin/env python
# these here programming codes are licensed under the gnu fearsome dude license.

# 1: hbase(main):001:0> create '500k-test', 'unit:'
# 2: $> hbase thrift start
# 3: $> python testdata-500k.py (~500 seconds on my hackintosh)

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

def write_data(client, table, n):
    """writes n rows."""
    rowkey_base = "artist-100-track-"
    ymd = '20090618'
    for trackid in range(0, n+1):
        trackid_padded = "%08d" % trackid
        rowkey = rowkey_base + trackid_padded + '-' + ymd
        mutations = []
        m = {}
        m['column'] = 'unit:' + 'scrobbles'
        m['value']  = str(int(random() * 120))
        mutations.append(Mutation(m))
        if (trackid % 1000 == 0):
            print '=> ' + rowkey
        client.mutateRow(table, rowkey, mutations)

if __name__ == '__main__':
    client, transport = setup_thrift_transport('localhost')
    write_data(client, '500k-test', 500000)
    transport.close()
