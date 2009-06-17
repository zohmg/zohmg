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
#
# the usermapper yields tuples of the form (ts, dimensions, units).
# this mapper wrapper turns them into tuples of the form:
# ((ts, p, permut, unit), value).  er, read the code please.
class Mapper(object):
    def __init__(self, usermapper, projections=None):
        self.usermapper = usermapper
        if projections == None:
            projections = Config().projections()
        self.projections = projections

    # helper for generating (per)mutations of a dictionary.
    # returns a list of 2**len(input) number of dicts, like so:
    # {'a':'x', 'b':'y'} => [{'a':'x', 'b':'y'}, {'a':'x', 'b':'all'},
    #                        {'a':'all', 'b':'y'}, {'a':'all', 'b':'all'}]
    def dict_permutations(self, dict_):
        dict = dict_.copy()

        # base case.
        if len(dict) == 1:
            all_dict = {dict.keys()[0] : 'all'}
            # dict     => {'agent': 'firefox'}
            # all_dict => {'agent': 'all'}
            return [dict, all_dict]


        # assume dict => {'agent' : 'firefox', 'country' : 'SE', 'http-status' : '200'}
        x  = dict.popitem()               # x => ('agent', 'firefox')
        xs = self.dict_permutations(dict) # xs => [{'http-status': '200', 'country': 'SE'}, {'http-status': '200', 'country': 'all'}, {'http-status': 'all', 'country': 'SE'}, {'http-status': 'all', 'country': 'all'}]

        # combine x and xs into a list.
        permuts = []
        for k,v in [x, (x[0], 'all')]:
            # k => 'agent'
            # v => 'firefox' and 'all'
            for b in xs:
                # b => {'http-status': '200', 'country': 'SE'}
                # add {'agent':'firefox'} or {'agent':'all'} to b.
                b[k] = v
                permuts.append(b.copy())
        return permuts

    # wrapper around the user's mapper.
    def __call__(self, key, value):
        # from the usermapper: a timestamp, a point in n-space, units and their values.
        for (timestamp, dimensions, units) in self.usermapper(key, value):
            for projection in self.projections:
                # for example, if projection => ('user', 'artist')
                # and dimensions => {'user':100, 'artist':2002, 'track':822010}
                # then reduced => {'user':100, 'artist':2002}
                reduced = {}
                for d in projection:  # dimensionality reduction.
                    reduced[d] = dimensions[d]
                for unit in units:
                    value = units[unit]
                    permutations = self.dict_permutations(reduced)
                    # if reduced => {'user':100, 'artist':2002}
                    # then permutations => [{'user':100, 'artist':2002},
                    #                        {'user':100, 'artist':'all'},
                    #                        {'user':'all', 'artist':2002},
                    #                        {'user':'all', 'artist':'all'}]
                    for permut in permutations:
                        yield (timestamp, projection, permut, unit), value
