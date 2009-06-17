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


if __name__ == "__main__":
    unittest.main()
