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

import os, sys, time
import simplejson as json
from zohmg.config import Config
from paste.request import parse_formvars

# add middleware directory to path.
sys.path.append(os.path.dirname(__file__))
import data_utils

# this is the application responsible for serving data.
class data(object):
    def __init__(self):
        self.config = Config()
        self.table = self.config.dataset()
        self.projections = self.config.projections()

    # answer query.
    def __call__(self, environ, start_response):
        print "[%s] Data, serving from table: %s." % (time.asctime(),self.table)

        params = parse_formvars(environ)
        # jsonp.
        try:    jsonp_method = params["jsonp"]
        except: jsonp_method = None

        data  = {}
        try:
            # fetch.
            start = time.time()
            data = data_utils.hbase_get(self.table, self.projections, params)
            elapsed = (time.time() - start)
            sys.stderr.write("hbase query+prep time: %s\n" % elapsed)
        except ValueError:
            print >>sys.stderr, "400 Bad Request: missing arguments."
            start_response('400 Bad Request', [('content-type', 'text/html')])
            return "Query is missing arguments."
        except Exception, e:
            print >>sys.stderr, "Error: ", e
            start_response('500 OK', [('content-type', 'text/html')])
            return "Sorry, I failed in serving you: " + str(e)

        # serve output.
        start_response('200 OK', [('content-type', 'text/x-json')])
        return data_utils.dump_jsonp(data, jsonp_method)
