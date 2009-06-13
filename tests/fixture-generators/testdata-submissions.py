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

table = 'submissions-test'

units = ['scrobbles', 'loves']
scaling = {'scrobbles': 1000, 'loves': 2}

users   = [120, 240, 360]
artists = [1001, 1002, 1003, 1004, 1005]

projections = [('user'), ('user','artist')]

hashes = {} # pre-compute hashes.
for u in users:
    hashes[u] = hash(u) % 255

def magic_computation(unit, dimension):
    return random() * hashes[dimension] * scaling[unit]


def generate_data(client):
    year="2009"
    for month in range(1,13):
        month = "%02d" % month
        for day in range(1,31):
            ymd = year + month + "%02d" % day
            for user in users:
                rowkeyarray = []
                rowkeyarray.append('user')
                rowkeyarray.append(str(user))
                rowkeyarray.append(ymd)
                rowkey = '-'.join(rowkeyarray)

                mutations = []
                for unit in units:
                    m = {}
                    m['column'] = "unit:" + unit
                    m['value']  = str(int(magic_computation(unit, user)))
                    mutations.append(Mutation(m))
                print rowkey + " +> " + str(len(mutations)) + " mutations."
                client.mutateRow(table, rowkey, mutations)


if __name__ == '__main__':
    client, transport = setup_transport('localhost')
    generate_data(client)
    transport.close()
