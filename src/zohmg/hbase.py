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
    def create_table(self, client, table_name, families=[]):
        """."""
        try:
            columns = []
            for family in families:
                column = ColumnDescriptor(family+":")
                columns.append(column)
            client.createTable(table_name, columns)

        except AlreadyExists:
            sys.stderr.write("oh noes, %s already exists.\n" % t)
            exit(2)
        except IOError, e:
            sys.stderr.write("bust: IOError: "+ str(e) + "\n")
            exit(3)
        except IllegalArgument, e:
            sys.stderr.write("error: " + str(e) + "\n")
            sys.stderr.write(" => bust\n")
            exit(4)
