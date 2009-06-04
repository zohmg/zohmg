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
from utils import *

# reads conf, creates table.
class Setup(object):
    def go(self):
        c = Config()
        dataset = c.config['dataset']

        cfs = []
        # each projection becomes a column-family,
        # i.e. "user-country-agent".
        for p in c.config['projections']:
            cfs.append(p)

        print "creating table '%s'" % dataset
        print " column families:"
        print "".join((map( lambda cf: "  + "+str(cf)+":\n" , cfs)))

        try:
            c = setup_transport("localhost")
        except:
            sys.stderr.write("could not setup thrift transport.\n")
            sys.stderr.write("is the thrift server turned on?\n")
            sys.exit(1)

        create_or_bust(c, dataset, cfs)
