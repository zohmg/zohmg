import string, sys, time
from random import Random
from hbase.ttypes import *


#
# HBase helpers
#
def setup_transport(host):
    from thrift import Thrift
    from thrift.transport import TSocket
    from thrift.transport import TTransport
    from thrift.protocol import TBinaryProtocol
    from hbase import Hbase
    transport = TSocket.TSocket(host, 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Hbase.Client(protocol)
    transport.open()
    return client


def create_or_bust(c, t, cfs=['fam']):
    print "creating table %s with %s or so cfs" % (t, len(cfs))
    try:
        cds = []
        for cf in cfs:
            cd = ColumnDescriptor({'name' : str(cf)+":" })
            cds.append(cd)
        c.createTable(t, cds)
    except AlreadyExists:
        print "oh noes, %s already exists." % t
        exit(2)
    except IOError:
        print "bust: IOError"
        exit(3)
    except IllegalArgument, e:
        print e
        print "create_or_bust => bust"
        exit(3)


def random_string(size):
    # subopt for larger sizes.
    if size > len(string.letters):
        return random_string(size/2)+random_string(size/2)
    return ''.join(Random().sample(string.letters, size))


def timing(func):
    def wrapper(*arg):
        t0 = time.time()
        r = func(*arg)
        elapsed = time.time() - t0
        return (elapsed*1000.00)
    return wrapper


def timing_p(func):
    def wrapper(*arg):
        t0 = time.time()
        r = func(*arg)
        elapsed = (time.time() - t0) * 1000.00
        print "=> %.2f ms" % elapsed
        return elapsed
    return wrapper


def disable(c, table):
    try:
        c.disableTable(table)
        print "%s disabled." % table
    except IOError, e:
        print "error: %s" % e
        return False
    return True


def enable(c, table):
    try:
        c.enableTable(table)
        print "%s enabled." % table
    except IOError, e:
        print "error: %s" % e
        return False
    return True


def drop(c, table):
    try:
        c.deleteTable(table)
        print "%s dropped." % table
    except IOError, e:
        print "IOError: %s" % e
        exit(128)
    except NotFound, e:
        print "NotFound: %s" % e


#
# General helpers
#
def compare_triples(p,q):
    """
    p and q are triples, like so: (4, 2, [..])
    sort by first element, then by the second one.
    return 1, 0, or -1 if x is larger than, equal to, or less than y.
    """
    a,b,c = p
    x,y,z = q
    if a > x: return 1
    if a < x: return -1
    if b > y: return 1
    if b < y: return -1
    return 0


def fail(msg,errno=1):
    print >>sys.stderr, msg
    exit(errno)


def http_get(url,query,host="localhost",port=8086):
    import httplib

    # connect to service and query for data.
    h = httplib.HTTPConnection(host,port)
    h.request("GET",url+"?"+query)
    r = h.getresponse()

    # return result or handle error.
    if r.status == 200:
        return r.read()
    else:
        return "Error: Encountered a \"%s %s\" while performing\nhttp://%s:%s%s?%s." % (
                    r.status, r.reason, host, port, url, query)


# strip whitespaces.
def strip(str):
    return str.strip()
