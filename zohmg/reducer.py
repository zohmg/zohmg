#Licensed to the Apache Software Foundation (ASF) under one
#or more contributor license agreements.  See the NOTICE file
#distributed with this work for additional information
#regarding copyright ownership.  The ASF licenses this file
#to you under the Apache License, Version 2.0 (the
#"License"); you may not use this file except in compliance
#with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing,
#software distributed under the License is distributed on an
#"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#KIND, either express or implied.  See the License for the
#specific language governing permissions and limitations
#under the License.

from zohmg.config import Config
import simplejson as json

class Reducer(object):
    def __init__(self):
        self.config = Config()

    def __call__(self, key, values):
        ts, ps, dims, unit = key
        value = sum(values)

        # rowkey: "unit-ymd".
        rk = '-'.join([unit, str(ts)])

        # construct column-family and qualifier strings.
        # it's important that we get the ordering right.
        cflist = []
        qlist  = []
        for p in ps:
            cflist.append(p)
            qlist.append(dims[p])
        cf = '-'.join(cflist)
        q  = '-'.join(qlist)

        # remember, we'll pass the output of this reducer to HBaseOutputReader.
        yield rk, json.dumps({cf+":"+q : {'value':value}})
