import string, sys, time
from random import Random

# TODO: move all hbase utils to it's own module.

#
# HBase helpers
#
def setup_transport(host):
    from thrift import Thrift
    from thrift.transport import TSocket
    from thrift.transport import TTransport
    from thrift.protocol import TBinaryProtocol
    from hbase import Hbase
    try:
        transport = TSocket.TSocket(host, 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = Hbase.Client(protocol)
        transport.open()
        return client
    except:
        raise


def create_or_bust(c, t, cfs=['fam']):
    from hbase.ttypes import *
    print "creating hbase table %s." % t
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
    print "ok."


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
def compare_triples(p, q):
    """
    p and q are triples, like so: (4, 2, ..)
    sort by first the element, then by the second. don't care about the third element.
    return 1, 0, or -1 if p is larger than, equal to, or less than q, respectively.
    """
    a, b, dontcare = p
    x, y, dontcare = q
    if a > x: return  1
    if a < x: return -1
    if b > y: return  1
    if b < y: return -1
    return 0


def fail(msg,errno=1):
    print >>sys.stderr, msg
    exit(errno)


# strip whitespaces.
def strip(str):
    return str.strip()
