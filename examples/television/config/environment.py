# path to yr hadoop directory.
HADOOP_HOME = '/home/fredrik/workspace/hadoop-0.20'

# jars for hadoop, hadoop streaming and hbase
# (you may need to 'ant package' in $HADOOP_HOME to build the streaming jar.)
CLASSPATH = (
  HADOOP_HOME + '/build/hadoop-0.20.1-dev-core.jar',
  HADOOP_HOME + '/build/contrib/streaming/hadoop-0.20.1-dev-streaming.jar',
  '/home/fredrik/workspace/hbase-trunk/build/hbase-0.20.0-dev.jar'
)
