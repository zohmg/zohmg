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


