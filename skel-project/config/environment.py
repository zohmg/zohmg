# path to yr hadoop directory.
HADOOP_HOME = '/opt/hadoop-0.20.0'

# jars for hadoop, hadoop streaming and hbase
# (you may need to 'ant package' in $HADOOP_HOME to build the streaming jar.)
CLASSPATH = (
  '/opt/hadoop-0.20.0/hadoop-0.20.0-core.jar',
  '/opt/hadoop-0.20.0/build/contrib/streaming/hadoop-0.20.0-streaming.jar',
  '/opt/hbase-0.20.0-alpha/hbase-0.20.0-alpha.jar'
)
