import os, sys


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
  '/home/hadoop/hadoop-0.19/hadoop-0.19.0-core.jar',
  '/home/hadoop/hadoop-0.19/build/contrib/streaming/hadoop-0.19.0-streaming.jar
  '/home/hadoop/hbase-0.19/hbase-0.19.0.jar'
)
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
            import errno
            msg = "E: Could not create project directories. "

            if ose.errno is errno.EEXIST:
                msg += "Directory '%s' already exists." % self.abspath
                self.__fail(msg)
            elif ose.errno is errno.EACCES:
                msg += "Permission denied to create '%s' in '%s'." % (self.path,os.path.dirname(self.abspath))
                self.__fail(msg)

            self.__fail(msg)

        # Create empty zohmg app identification file.
        self.__write_to_file(self.abspath+"/.zohmg","")

        # Create skeleton config/datasets.yaml
        datasetconfig = "project_name: %s\n" % self.basename \
                      + "dimensions:\n  -d0\n  -d1\n" \
                      + "projections:\n  p0:\n    -d0\n    -d1\n" \
                      + "units:\n  u0\n"
        self.__write_to_file(self.abspath+"/config/datasets.yaml", datasetconfig)

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
        except:
            self.__fail("E: Internal error, could not write to '%s'." % file)
