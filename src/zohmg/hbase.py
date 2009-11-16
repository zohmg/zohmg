import sys
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from hbase_thrift import Hbase
from hbase_thrift.ttypes import ColumnDescriptor
from hbase_thrift.ttypes import AlreadyExists, IOError, IllegalArgument

class ZohmgHBase:

    @classmethod
    def transport(self, host='localhost'):
        try:
            transport = TSocket.TSocket(host, 9090)
            transport = TTransport.TBufferedTransport(transport)
            protocol  = TBinaryProtocol.TBinaryProtocol(transport)
            client = Hbase.Client(protocol)
            transport.open()
            return client
        except ImportError, e:
            sys.stderr.write(str(e)+'\n')
            sys.exit(8)
        except Exception, e:
            print "e: " + str(e.__class__) + " ^ " + str(e)
            sys.stderr.write("could not setup thrift transport.\n")
            sys.stderr.write("is the thrift server switched on?\n")
            sys.exit(16)


    @classmethod
    def create_table(self, table_name, families=[], client=None):
        """."""
        if not client:
            # default to localhost.
            client = ZohmgHBase.transport("localhost")

        try:
            columns = []
            for family in families:
                column = ColumnDescriptor(family+":")
                columns.append(column)
            client.createTable(table_name, columns)

        except AlreadyExists:
            sys.stderr.write("oh noes, %s already exists.\n" % table_name)
            exit(2)
        except IOError, e:
            sys.stderr.write("bust: IOError: "+ str(e) + "\n")
            exit(3)
        except IllegalArgument, e:
            sys.stderr.write("error: " + str(e) + "\n")
            sys.stderr.write(" => bust\n")
            exit(4)

    @classmethod
    def delete_table(self, table_name, client=None):
        if not client:
            # default to localhost.
            client = ZohmgHBase.transport("localhost")
        ZohmgHBase.disable_table(table_name, client) and \
        ZohmgHBase.drop_table(table_name, client)

    @classmethod
    def disable_table(self, table_name, client=None):
        try:
            client.disableTable(table_name)
            print "%s disabled." % table_name
        except IOError, e:
            print "error: %s" % e
            raise
        return True

    @classmethod
    def drop_table(self, table_name, client=None):
        try:
            client.deleteTable(table_name)
            print "%s dropped." % table_name
        except IOError, e:
            print "IOError: %s" % e
            raise
        return True
