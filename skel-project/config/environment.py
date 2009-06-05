# path to yr hadoop directory.
HADOOP_HOME = '/opt/hadoop-0.19.1'

# jars for hadoop, hadoop streaming and hbase
# (you may need to 'ant package' in $HADOOP_HOME to build the streaming jar.)
CLASSPATH = (
  '/opt/hadoop-0.19.1/build/hadoop-0.19.2-dev-core.jar',
  '/opt/hadoop-0.19.1/build/contrib/streaming/hadoop-0.19.2-dev-streaming.jar',
  '/opt/hbase-0.19.3/build/hbase-0.19.3.jar'
)
