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
import zohmg.data

class TestData(unittest.TestCase):
    def test_find_suitable_projection(self):
        projections = [['user'], ['user','artist'], ['artist', 'user']]

        ## find_suitable_projection() should:

        # find the correct projection when there's a single matching projection.
        p = zohmg.data.find_suitable_projection(projections, 'user', {})
        self.assertEqual(p, ['user'])

        # get the ordering right - both ['user','artist'] and ['artist', 'user']
        # satisfy a query for 'artist', but the latter is more efficient to read from.
        p = zohmg.data.find_suitable_projection(projections, 'artist', {})
        self.assertEqual(p, ['artist', 'user'])

        # return None if there is no match.
        p = zohmg.data.find_suitable_projection(projections, 'non-existant', {})
        self.assertEqual(p, None)

    def test_dump_jsonp(self):
        json = zohmg.data.dump_jsonp([{'a':'x', 'something':700}])
        expected = '[{"a": "x", "something": 700}]'
        self.assertEquals(json, expected)

    def test_query(self):
        # call query() with no arguments.
        from zohmg.data import MissingArguments
        self.assertRaises(MissingArguments, zohmg.data.query, 'no-table', [], {})

        # TODO:
        # query servers json.
        # sometimes jsonp.


    def test_scan(self):
        # TODO: mock scanner, assert correctness of scan().
        pass


    def test_hbase_get(self):
        table = 'test' # must there be test data, then?
        projections = [['user']]
        params = {}


        #        r = zohmg.data.hbase_get(table, projections, params)
        #        self.assert_equal(r, 'wha?')



    def test_rowkey_formatter(self):
        projection = ['user']
        d0 = 'user'
        d0v = ['']
        filters = {}
        t0 = "20090601"
        t1 = "20090631"

        expected_startrow = "user-all-20090601"
        expected_stoprow  = "user-all-20090631~"

        startrow, stoprow = zohmg.data.rowkey_formatter(projection, d0, d0v, filters, t0, t1)

        self.assertEquals(startrow, expected_startrow)
        self.assertEquals(stoprow, expected_stoprow)

    def test_rowkey_interpreter(self):
        rowkey = 'artist-97930-track-102203-20090601'
        expected = ('20090601', {'artist': '97930', 'track': '102203'})
        self.assertEqual(expected, zohmg.data.rowkey_interpreter(rowkey))

        rowkey = 'artist-97930-track-102203-20090601223000'
        expected = ('20090601223000', {'artist': '97930', 'track': '102203'})
        self.assertEqual(expected, zohmg.data.rowkey_interpreter(rowkey))


    def test_dict_addition(self):
        a = {'x': 1, 'y': 1}; aprim = a.copy()
        b = {'x': 2, 'z': 1}; bprim = b.copy()
        expected = {'x': 3, 'y': 1, 'z': 1}

        self.assertEquals(expected, zohmg.data.dict_addition(a,b))
        # make sure nothing was changed.
        self.assertEquals(a, aprim)
        self.assertEquals(b, bprim)


if __name__ == "__main__":
    unittest.main()
