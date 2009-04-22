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
    print zohmg + " help"

def print_version():
    v = '0.0.30.4204-0'
    print "zohmg version " + v

def print_help():
    # TODO: offer help.
    print "wha?"

# cli entry-point.
def zohmg():
    try:
        # read the first argument.
        cmd = sys.argv[1]
    except:
        usage()
        sys.exit(1)

    if   cmd == "create":  create()
    elif cmd == "setup":   setup()
    elif cmd == 'process': process()
    elif cmd == 'serve':   serve()
    elif cmd == "version" or cmd == "--version": print_version()
    elif cmd == "help"    or cmd == '--help':    print_help()
    else:
        usage()


def create():
    from zohmg.create import Create
    try:
        path = sys.argv[2]
    except:
        usage("create needs an argument.")
        sys.exit(1)

    Create(path)


def setup():
    refuse_to_act_in_nonzohmg_directory()
    from zohmg.setup import Setup
    Setup().go()


def process():
    refuse_to_act_in_nonzohmg_directory()
    from zohmg.process import Process
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

    Process().go(mapperpath, inputdir, dumbo_args)


def serve():
    refuse_to_act_in_nonzohmg_directory()
    from zohmg.serve import Serve
    # check for optional argument.
    try:    port = sys.argv[2]
    except: port = 8086 # that's ok.

    Serve(port)


# exits if 'zohmg' was run in a directory without the special .zohmg-file.
def refuse_to_act_in_nonzohmg_directory():
    cwd = os.getcwd()
    if not os.path.exists(cwd+"/.zohmg"):
        print "hey!, this is not a proper zohmg app."
        sys.exit(1)
