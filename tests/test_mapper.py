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

import unittest
from zohmg.mapper import Mapper

# void usermapper.
def m(key, value):
    pass

# mock of usermapper.
def mock_mapper(k, v):
    ymd = '20090618'
    yield (ymd, {'agent':'firefox', 'path':'/about'}, {'hit':1})

class TestMapper(unittest.TestCase):
    def test_dict_permutations(self):
        mapper = Mapper(m, []) # setup with void mapper and empty projection list.

        p = mapper.dict_permutations({'agent': 'firefox'})
        self.assertEqual(p, [{'agent': 'firefox'}, {'agent': 'all'}])

        p = mapper.dict_permutations({'a':'x', 'b':'y'})
        expected = [{'a':'x', 'b':'y'}, {'a':'x', 'b':'all'}, {'a':'all', 'b':'y'}, {'a':'all', 'b':'all'}]
        self.assertEqual(p, expected)

        p = mapper.dict_permutations({'agent' : 'firefox', 'country' : 'SE', 'http-status' : '200', 'path':'/'})
        expected = [{'http-status': '200', 'path': '/', 'agent': 'firefox', 'country': 'SE'}, {'http-status': '200', 'path': '/', 'agent': 'all', 'country': 'SE'}, {'http-status': '200', 'path': 'all', 'agent': 'firefox', 'country': 'SE'}, {'http-status': '200', 'path': 'all', 'agent': 'all', 'country': 'SE'}, {'http-status': '200', 'path': '/', 'agent': 'firefox', 'country': 'all'}, {'http-status': '200', 'path': '/', 'agent': 'all', 'country': 'all'}, {'http-status': '200', 'path': 'all', 'agent': 'firefox', 'country': 'all'}, {'http-status': '200', 'path': 'all', 'agent': 'all', 'country': 'all'}, {'http-status': 'all', 'path': '/', 'agent': 'firefox', 'country': 'SE'}, {'http-status': 'all', 'path': '/', 'agent': 'all', 'country': 'SE'}, {'http-status': 'all', 'path': 'all', 'agent': 'firefox', 'country': 'SE'}, {'http-status': 'all', 'path': 'all', 'agent': 'all', 'country': 'SE'}, {'http-status': 'all', 'path': '/', 'agent': 'firefox', 'country': 'all'}, {'http-status': 'all', 'path': '/', 'agent': 'all', 'country': 'all'}, {'http-status': 'all', 'path': 'all', 'agent': 'firefox', 'country': 'all'}, {'http-status': 'all', 'path': 'all', 'agent': 'all', 'country': 'all'}]
        self.assertEqual(p, expected)

    def test_mapper(self):
        mapper = Mapper(mock_mapper, [['agent']])
        output = list(mapper(0, 'bogus value'))
        expected  = []
        expected += [(('20090618', ['agent'], {'agent': 'firefox'}, 'hit'), 1)]
        expected += [(('20090618', ['agent'], {'agent': 'all'}, 'hit'), 1)]
        self.assertEqual(output, expected)

        mapper = Mapper(mock_mapper, [['agent','path'], ['path'], ['agent']])
        output = list(mapper(0, 'bogus value'))
        expected  = []
        expected += [(('20090618', ['agent', 'path'], {'path': '/about', 'agent': 'firefox'}, 'hit'), 1)]
        expected += [(('20090618', ['agent', 'path'], {'path': '/about', 'agent': 'all'}, 'hit'), 1)]
        expected += [(('20090618', ['agent', 'path'], {'path': 'all', 'agent': 'firefox'}, 'hit'), 1)]
        expected += [(('20090618', ['agent', 'path'], {'path': 'all', 'agent': 'all'}, 'hit'), 1)]
        expected += [(('20090618', ['path'], {'path': '/about'}, 'hit'), 1)]
        expected += [(('20090618', ['path'], {'path': 'all'}, 'hit'), 1)]
        expected += [(('20090618', ['agent'], {'agent': 'firefox'}, 'hit'), 1)]
        expected += [(('20090618', ['agent'], {'agent': 'all'}, 'hit'), 1)]
        self.assertEqual(output, expected)

if __name__ == "__main__":
    unittest.main()
