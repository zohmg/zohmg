import os, sys

from zohmg.utils import fail


DIRS = ["config","lib","mappers","transformers"]

# config/environment.py
ENV_SCRIPT = """# Please define the following environment variables.

# Path to Hadoop directory.
HADOOP_HOME = ''

# Path to HBase directory.
HBASE_HOME = ''

# Jars for Hadoop Core, Hadoop Streaming and HBase
CLASSPATH = (
  # be sure to set these correctly!
  '/home/hadoop/hadoop-0.19/hadoop-0.19.0-dev-core.jar',
  '/home/hadoop/hadoop-0.19/build/contrib/streaming/hadoop-0.19.0-dev-streaming.jar',
  '/home/hadoop/hbase-0.19/hbase-0.19.0-dev.jar'
)
"""

README = """This is your zohmg application! Write mappers and put them in the mappers directory,
configure things in the config directory and run 'zohmg setup' to set things up.
"""


class Create(object):
    def __init__(self, path):
        self.basename = os.path.basename(path)
        self.path = path
        self.abspath = os.path.abspath(path)

        print "Creating %s" % self.basename

        # Create project directories with 0755.
        try:
            os.mkdir(self.abspath)
            for dir in DIRS:
                os.mkdir(self.abspath+"/"+dir)
        # Something went wrong, act accordingly.
        except OSError, ose:
            msg = "E: Could not create project directories. %s" % ose.strerror
            fail(msg,ose.errno)

        # Create empty zohmg app identification file.
        self.__write_to_file(self.abspath+"/.zohmg","")

        # Create skeleton config/datasets.yaml
        datasetconfig = "project_name: %s\n" % self.basename \
                      + "dimensions:\n  -d0\n  -d1\n" \
                      + "projections:\n  p0:\n    -d0\n    -d1\n" \
                      + "units:\n  u0\n"
        self.__write_to_file(self.abspath+"/config/datasets.yaml", datasetconfig)

        # Write README.
        self.__write_to_file(self.abspath+"/README", README)

        # Put environment script down.
        self.__write_to_file(self.abspath+"/config/environment.py", ENV_SCRIPT)

        print "ok."


    # something did not work during project creation, clean up.
    def __fail(self,msg):
        print >>sys.stderr, msg
        exit(1)


    def __write_to_file(self,file,str):
        try:
            f = open(file,"w")
            f.write(str)
            f.close()
        except IOError, ioe:
            msg = "E: Internal error. %z." % ioe.strerror
            fail(msg,ioe.errno)
