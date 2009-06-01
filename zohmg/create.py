from zohmg.utils import fail
import os, sys

# FIXME: temporarily disabled 'clients'
DIRS = ["config","lib","mappers","transformers"]

# config/environment.py
ENV_SCRIPT = """# Please define the following environment variables.

# Path to Hadoop directory.
HADOOP_HOME = '/opt/hadoop-0.19.1'

# Jars for Hadoop Core, Hadoop Streaming and HBase
CLASSPATH = (
  # be sure to set these correctly!
  '/opt/hadoop-0.19.1/build/hadoop-0.19.2-dev-core.jar',
  '/opt/hadoop-0.19.1/build/contrib/streaming/hadoop-0.19.2-dev-streaming.jar',
  '/opt/hbase-0.19.3/build/hbase-0.19.3.jar'
)
"""

README = """This is your zohmg application!

Configure config/dataset.yaml to match your data,
run 'zohmg setup' to create an hbase table,
write a mapper and run with 'zohmg import'.

Take a look in /usr/local/share/zohmg/doc for further documentation
and /usr/local/share/zohmg/examples for, yes, examples.
"""

CLIENT = """<html>
<body>
Static files here will be served from the url http://host:port/client/filename.
</body>
</html>
"""

MAPPER = """# identity mapper.
def map(key, value):
    # egads!
"""

TRANSFORMER = """# identity transformer.
def transform(payload):
    return payload
"""


class Create(object):
    def __init__(self, path):
        self.basename = os.path.basename(path)
        self.abspath  = os.path.abspath(path)

        
        DATASET= """
dataset:
  %s

dimensions:
  - d0
  - d1

projections:
  - d0
  - d0-d1

units:
  -u0
""" % (self.basename)

        sys.stdout.write("Creating %s... " % self.basename)

        # Create project directories with 0755.
        try:
            os.mkdir(self.abspath)
            for dir in DIRS:
                os.mkdir(self.abspath+"/"+dir)
        # Something went wrong, act accordingly.
        except OSError, ose:
            msg = "Error: Could not create project directories. %s" % ose.strerror
            fail(msg, ose.errno)

        # Create .zohmg, README, client, environment, mapper and transformer.
        self.__write_to_file('.zohmg')
        self.__write_to_file('README', README)
        #self.__write_to_file("clients/client.html",CLIENT)
        self.__write_to_file('config/environment.py', ENV_SCRIPT)
        self.__write_to_file('mappers/identity_mapper.py', MAPPER)
        self.__write_to_file("transformers/identity_transformer.py",TRANSFORMER)
        self.__write_to_file("config/dataset.yaml", DATASET)
        # TODO: consider using Config.config_file instead of hardcoded path.

        print "ok."


    def __write_to_file(self, filename, contents = ''):
        file = self.abspath + '/' + filename
        try:
            f = open(file, "w")
            f.write(contents)
            f.close()
        except IOError, ioe:
            msg = "Kernel malfunction: %s (%s)." % (ioe.strerror, file)
            fail(msg, ioe.errno)
