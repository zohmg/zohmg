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

from zohmg.config import Config
import simplejson as json

# the output of this reducer is interpreted by HBaseOutputReader.
class Reducer(object):
    def __init__(self):
        self.config = Config()

    def __call__(self, key, values):
        timestamp, projection, dimensions, unit = key
        value = sum(values)

        if value == 0:
            return

        # encode dimensions and their attributes in the rowkey.
        # (it's important that we get the ordering right.)
        rowkeyarray = []
        for d in projection:
            rowkeyarray.append(d)
            rowkeyarray.append(dimensions[d])
        rowkeyarray.append(str(timestamp))
        rowkey = '-'.join(rowkeyarray)
        # rowkey => 'artist-97930-track-102203-20090601'

        columnfamily = "unit:"
        cfq = columnfamily + unit
        # cfq => 'unit:scrobbles'

        json_payload = json.dumps({cfq : {'value': value}})
        # json_payload => '{"unit:scrobbles": {"value": 1338}}'

        yield rowkey, json_payload
