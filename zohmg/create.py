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
    # '/path/to/file.jar',
)
"""


class Create(object):
    def __init__(self, path):
        self.path = path
        self.abspath = os.path.abspath(path)

        print "Creating zohmg app in %s ..." % self.path

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

        # Create empty config/datasets.yaml
        self.__write_to_file(self.abspath+"/config/datasets.yaml","")

        # Put environment script down.
        self.__write_to_file(self.abspath+"/config/environment.py",ENV_SCRIPT)


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
