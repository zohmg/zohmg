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

# MIDDLEWARE DATA HELLO.

import os, sys, time
import simplejson as json

from paste.request import parse_formvars

import zohmg.data
from zohmg.config import Config

def json_of(error_msg='wha?', status_code=400, callback=None):
    structure = {'error_msg': error_msg, 'status_code': status_code}
    jsondata = json.dumps(structure)
    if callback:
        return callback+"("+jsondata+")"
    else:
        return jsondata

# data application serving at /data.
class data(object):
    def __init__(self, dataset=None, projections=None):
        if dataset == None or projections == None:
            config = Config()

        if dataset == None:
            self.table = config.dataset()
        else:
            self.table = dataset

        if projections == None:
            self.projections = config.projections()
        else:
            self.projections = projections

    # answer query.
    def __call__(self, environ, start_response):
        mime_type = 'text/plain' # under what type we serve json.
        content_type = [('content-type', mime_type)]

        # TODO: check that table exists, exit gracefully if not.

        # interpret the environment.
        params = parse_formvars(environ)

        # error callback?
        # (hm! can not do json error callbacks on error codes other than 200.)
        try:    errorcallback = params['jsonperror']
        except: errorcallback = None

        try:
            # hbase query.
            start = time.time()
            json = zohmg.data.query(self.table, self.projections, params)

        except zohmg.data.DataNotFound, (instance):
            print >>sys.stderr, "Data not found: ", instance.error
            start_response('200 OK', content_type)
            return json_of("data not found: " + instance.error, 200, errorcallback)

        except zohmg.data.MissingArguments, (instance):
            print >>sys.stderr, "400 Bad Request: missing arguments."
            #start_response('400 Bad Request', content_type)
            start_response('200 OK', content_type)
            return json_of("Query is missing arguments: " + instance.error, 400, errorcallback)
            # TODO: print list of required arguments.

        except zohmg.data.NoSuitableProjection, (instance):
            print >>sys.stderr, "400 Bad Request: No suitable projection. ", instance.error
            #start_response('400 Bad Request', content_type)
            start_response('200 OK', content_type)
            return json_of(" " + instance.error, 400, errorcallback)

        except Exception, e:
            print >>sys.stderr, "Error: ", e
            #start_response('500 Internal Server Error', content_type)
            start_response('200 OK', content_type)
            return json_of("egads!, I failed in serving you: " + str(e), 500, errorcallback)

        elapsed = (time.time() - start)
        sys.stderr.write("hbase query+prep: %s\n\n" % elapsed)

        # serve output.
        start_response('200 OK', content_type) # or text/x-json
        return json
