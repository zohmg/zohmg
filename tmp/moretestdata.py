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

countries = ['US', 'SE', 'DE', 'ES', 'GB', 'FR', 'IT', 'DK', 'all']
usertypes = ['anon', 'user', 'all']
agents = ['ff', 'ie', 'safari', 'opera', 'all']

hashes = {} # pre-compute country hashes.
for c in countries: hashes[c] = hash(c) % 255

client, transport = setup_transport('localhost')

for year in range(2009, 2020):
    year = str(year)
    for month in range(1,13):
        month = "%02d" % month
        for day in range(1,31):
            ymd = year + month + "%02d" % day
            for unit in units:
                rk = unit + "-" + ymd
                mutations = []
                # no sparseness here!
                for c in countries:
                    for u in usertypes:
                        for a in agents:
                            m = {}
                            q = '-'.join([c,u,a])
                            m['column'] = "country-usertype-useragent:"+q
                            print m['column']
                            extra_scaling = 1
                            if 'all' in [c,u,a]: extra_scaling = 20
                            m['value']  = str(int(random() * hashes[c] * scaling[unit] * extra_scaling))
                            mutations.append(Mutation(m))
                print rk + " +> " + str(len(mutations)) + " mutations."
                client.mutateRow(table, rk, mutations)

transport.close()
