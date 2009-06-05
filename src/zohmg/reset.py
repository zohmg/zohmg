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

import sys
from zohmg.setup import Setup
from zohmg.config import Config
from zohmg.utils import setup_transport, disable, drop

class Reset(object):
    def please(self):
        host = 'localhost'
        table = Config().dataset()

        # confirm.
        print "reset will *wipe all data* in dataset '%s'." % table
        print "ARE YOU QUITE SURE? ('yes' to confirm.)"

        response = sys.stdin.readline().strip()
        if response.lower() not in ["yes", "yes!"]:
            print 'phew!'
            sys.exit(0)

        # disable+drop.
        print "ok, wiping!"
        c = setup_transport(host)
        disable(c, table)
        drop(c, table)
        # TODO: handle case where table does not exist.

        # recreate (with the help of our dear friend setup).
        print
        print "recreating."
        Setup().go()

        print
        print "%s reset'd" % table

