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
for c in countries:
    hashes[c] = hash(c) % 255

client, transport = setup_transport('localhost')

def magic_computation(unit, dimension):
    return random() * hashes[dimension] * scaling[unit]



year="2009"
for month in range(1,13):
    month = "%02d" % month
    for day in range(1,31):
        ymd = year + month + "%02d" % day
        for unit in units:    
            rk = unit + "-" + ymd
            mutations = []
            for country in countries:
                m = {}
                m['column'] = "country:" + country
                m['value']  = str(int(magic_computation(unit, country)))
                mutations.append(Mutation(m))
            print rk + " +> " + str(len(mutations)) + " mutations."
            client.mutateRow(table, rk, mutations)

transport.close()
