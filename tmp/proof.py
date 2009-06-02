#Licensed to the Apache Software Foundation (ASF) under one
#or more contributor license agreements.  See the NOTICE file
#distributed with this work for additional information
#regarding copyright ownership.  The ASF licenses this file
#to you under the Apache License, Version 2.0 (the
#"License"); you may not use this file except in compliance
#with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing,
#software distributed under the License is distributed on an
#"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#KIND, either express or implied.  See the License for the
#specific language governing permissions and limitations
#under the License.

#!/usr/bin/python

import os, sys, yaml
from zohmg import Config, Mapper, Reducer


def usage():
    print "usage: " + sys.argv[0] + " <map.py> <dumboesque arguments>"


if __name__ == "__main__":
    print "me: " + sys.argv[0]

    envkey="ZOHMG_USER_MAPPER"
    user_mapper = os.getenv(envkey)
    if user_mapper == None:
        # first time around, it seems.
        print "first time around."
        try:
            mapper=sys.argv[1]
        except IndexError:
            usage()
            sys.exit(1)
        # make link from lib/usermapper.py to user's actual mapper.
        try: x = os.remove('lib/usermapper.py')
        except: pass
        y = os.symlink(mapper, 'lib/usermapper.py')
        
        os.putenv(envkey, mapper)
        print "arguments are: %s" % str(sys.argv)
        print "sending: %s" % sys.argv[2:]
        os.system("dumbo start %s %s" % (sys.argv[0], " ".join(sys.argv[2:])))
    else:
        # 'dumbo start' invoked us. thanks for that.
        import dumbo
        from usermapper import map as usermap
        dumbo.run(Mapper(usermap), Reducer, dumbo.sumreducer)

# open problems:
#  send user's mapper inside file.
#  keep 'all'-records.


