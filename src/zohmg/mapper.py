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

# exploding mapper!
# every emitted record from the usermapper is expanded
# to len(projections) * len(units) * 2^len(reduced) records.
class Mapper(object):
    def __init__(self, usermapper):
        self.usermapper = usermapper
        self.projections = Config().projections()

    # helper for generating all permutations of a dictionary.
    def dict_permutations(self, dict_):
        dict = dict_.copy()

        # base case.
        if len(dict) == 1:
            # i.e., {'agent': 'firefox'} => [{'agent': 'firefox'}, {'agent': 'all'}]
            return [dict, {dict.keys()[0] : 'all'}]

        x  = dict.popitem()
        xs = self.dict_permutations(dict)

        permuts = []
        for a in [x, (x[0], 'all')]:
            for b in xs: # b => {'agent': "firefox", 'country': "US"}
                b[a[0]] = a[1] # add a to b.
                permuts.append(b.copy())
        return permuts

    # wrapper around the user's mapper.
    def __call__(self, key, value):
        # from the usermapper: a timestamp, a point in n-space, units and their values.
        for (ts, point, units) in self.usermapper(key, value):
            for p in self.projections:
                reduced = {}
                for d in p:  # dimensionality reduction.
                    reduced[d] = point[d]
                for u in units:
                    value = units[u]
                    for permut in self.dict_permutations(reduced):
                        yield (ts, p, permut, u), value
