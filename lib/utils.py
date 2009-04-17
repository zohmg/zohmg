import httplib, socket, string, sys, time
from random import Random

# HTTP headers for HBase REST communication.
# Required: Accept
headers = {"Accept":"*/*",
           "User-Agent":"Zohmg (utils)/0.0.1"
          }


def create_table_xml(name,colfams):
    # header
    data = '<?xml version="1.0" encoding="UTF-8"?>\n<table>\n'
    data += "    <name>%s</name>\n    <columnfamilies>\n" % name
    # column-families
    for colfam in colfams:
        data += "    <columnfamily><name>%s:</name></columnfamily>\n" % colfam
    # tail
    data += "    </columnfamilies>\n</table>\n"
    return data


def create_or_bust(name, cfs=['fam'],host="localhost",port=60050):
    print "I: creating table %s with %s or so cfs" % (name, len(cfs))
    creation_payload = create_table_xml(name,cfs)
    # hardwired hbase REST host and port
    # TODO: put this in config and read it
    # connect to HBase REST and POST our table creation data
    try:
        conn = httplib.HTTPConnection(host,port)
        conn.request("POST","/api/",creation_payload,headers)
        response = conn.getresponse()
        if not response.status is 200:
            print >> sys.stderr, "E: could not create table %s." % name
            exit(2)
    except socket.error:
        print >> sys.stderr, "E: Could not connect to HBase REST on %s:%s" % (host,port)


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


def change_table_mode(mode,table,host,port):
    try:
        conn = httplib.HTTPConnection(host,port)
        conn.request("POST","/api/"+table+"/"+mode,"",headers) # alters table mode
        response = conn.getresponse()
        if not response.status is 202:
            print >> sys.stderr, "E: Could not %s table %s." % (mode,table)
    except socket.error:
        print >> sys.stderr, "E: Could not connect to HBase REST on %s:%s." % (host,port)


def enable(table,host="localhost",port="60050"):
    print "I: Enabling table %s." % table
    change_table_mode("enable",table,host,port)

def disable(table,host="localhost",port="60050"):
    print "I: Disabling table %s." % table
    change_table_mode("disable",table,host,port)


def drop(table,host="localhost",port=60050):
    print "I: Dropping table %s." % table
    try:
        conn = httplib.HTTPConnection(host,port)
        conn.request("DELETE","/api/"+table,"",headers) # drops table
        response = conn.getresponse()
        if not response.status is 202:
            print >> sys.stderr, "E: Could not drop table %s" % table
    except socket.error:
        print >> sys.stderr, "E: Could not connet to HBase REST on %s:%s." % (host,port)
