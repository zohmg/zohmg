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

# add middleware dir and import data_utils.
sys.path.append(os.path.dirname(__file__))
import data_utils

# TODO: use this.
class transform(object):
    def __init__(self):
        self.config = Config()
        self.table = self.config.dataset()
        self.projections = self.config.projections()

    def __call__(self,environ,start_response):
        project_dir = environ["zohmg_project_dir"]
        url_parts = environ["PATH_INFO"][1:-1].split("/") # trim pre- and appending /

        print "[%s] Transform, serving from %s." % (time.asctime(),project_dir)

        if len(url_parts) > 1:
            start_response("404 Not Found",[("Content-type","text/html")])
            return "Too many levels in path: %s." % environ["PATH_INFO"]
        else:
            # import user transformer.
            sys.path.append(project_dir) # add cwd so we can import from there.
            usertransformer = __import__("transformers/"+url_parts[0])
            transform = usertransformer.transform

        payload = data_utils.hbase_get(self.table,self.projections,environ)
        if payload:
            start_response("200 OK",[("Content-type","text/html")])
            return data_utils.dump_jsonp(transform(payload))
        else:
            start_response("404 Not Found",[("Content-type","text/html")])
            return "Bad query or no data found."
