import sys, os

def usage(reason = None):
    zohmg = os.path.basename(sys.argv[0])
    if reason:
        print "error: " + reason
    print "usage:"
    print zohmg + " create <dir>"
    print zohmg + " setup"
    print zohmg + " process <mapper> <hdfs-input-dir>"
    print zohmg + " serve [--port <port>]"
        
# the command line interface uses this as its entry-point.
def zohmg():
    try:
        cmd=sys.argv[1]
    except:
        usage()
        sys.exit(1)
      
    if cmd == "create":
        try:
            path = sys.argv[2]
        except:
            usage("create needs an argument.")
            sys.exit(1)
        from zohmg.create import Create
        Create(path)

    elif cmd == "setup":
        from zohmg.setup import Setup
        Setup().go()

    elif cmd == 'process':
        try:
            # check for two arguments,
            mapper = sys.argv[2]
            # (works only with relative paths for now.)
            mapperpath = os.path.abspath(".")+"/"+mapper
            inputdir = sys.argv[3]
            dumbo_args = sys.argv[4:]
        except:
            usage("%s needs two arguments." + cmd)
            sys.exit(1)
        from zohmg.process import Process
        Process().go(mapperpath, inputdir, dumbo_args)

    elif cmd == 'serve':
        # check for optional argument.
        try:    port = sys.argv[2]
        except: port = 8086 # that's ok.
        from zohmg.serve import Serve
        Serve(port)

    else:
        usage()

