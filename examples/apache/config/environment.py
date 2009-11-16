HADOOP_HOME = '/usr/local/hadoop'
HBASE_HOME  = '/usr/local/hbase'

# jars for hadoop, hadoop streaming and hbase
# (you may need to 'ant package' in $HADOOP_HOME to build the streaming jar.)
CLASSPATH = (
  HADOOP_HOME + '/' + 'hadoop-0.20.1-core.jar',
  HADOOP_HOME + '/' + 'build/contrib/streaming/hadoop-0.20.2-dev-streaming.jar',
  HBASE_HOME  + '/' + 'hbase-0.20.1.jar'
)
