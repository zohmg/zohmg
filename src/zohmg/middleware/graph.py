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

import time

class graph(object):
    """
    This application serves static files from the 'graph' directory in share.
    """
    def __call__(self, environ, start_response):
        from paste.urlparser import make_static
        # TODO: all hardcoded paths *will* break eventually.
        graph_dir = '/usr/local/share/zohmg/graph'
        graph = make_static({}, graph_dir)
        return graph(environ, start_response)
