#!/bin/bash
# Automagically install Hadoop and HBase in /opt or --prefix=PREFIX.
# Also, patch Hadoop with HADOOP-1722 and HADOOP-5450.

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

# TODO: use automatic mirror selection of ${hadoop,hbase}_url
# potential problem: apache seems to mirror only the very latest point release :-(


if [ $EUID -ne 0 ]; then
	echo "you need to be root. please sudo."
	exit 1
fi

# set default variables.
prefix="/opt"
version="0.20.0" # for streaming jar.
hadoop_version="hadoop-0.20.0"
hbase_version="hbase-0.20.0-alpha"

hadoop_tar="$hadoop_version.tar.gz"
hadoop_url="http://apache.mirror.infiniteconflict.com/hadoop/core/$hadoop_version/$hadoop_tar"
# or from http://www.apache.org/dyn/closer.cgi/hadoop/core/

##hbase_tar="$hbase_version.tar.gz"
##hbase_url="http://apache.mirror.infiniteconflict.com/hadoop/hbase/$hbase_version/$hbase_tar"
# or from http://www.apache.org/dyn/closer.cgi/hadoop/hbase

# using the alpha for now
hbase_tar="hbase-0.20.0-alpha.tar.gz"
hbase_url="http://people.apache.org/~stack/hbase-0.20.0-alpha/$hbase_tar"


# Dumbo (http://github.com/klbostee/dumbo) needs 1722 and 5450.
# (disable patching with --no-patches)

# HADOOP-1722  Make streaming to handle non-utf8 byte array - ASF JIRA
# https://issues.apache.org/jira/browse/HADOOP-1722
patch_1722="HADOOP-1722-v6.patch"
patch_1722_url="http://issues.apache.org/jira/secure/attachment/12400123/$patch_1722"

# Add support for application-specific typecodes to typed bytes
# https://issues.apache.org/jira/browse/HADOOP-5450
patch_5450="HADOOP-5450.patch"
patch_5450_url="http://issues.apache.org/jira/secure/attachment/12401846/$patch_5450"

install_log="/tmp/hadoop-hbase-install.log"
install_tmplog=$(mktemp /tmp/hadoop-hbase-install.tmp.log.XXXXXXXX)


# helpers.

# execute $1 and exit if it failed, displaying $2.
# TODO: the third argument is ignored. why? what was its purpose?
function exec_and_log() {
	# setup variables.
	command=$1

	[ "x" = "x$2" ] && msg="Error: Could not execute $command." || msg=$2

	# execute and log to intermediate.
	# FIXME: doesn't seem to log stderr
	# FIXME: doesn't retain return code when using pipes
	$1 # | tee "$install_tmplog" | cat
	ret=$?

	# log.
	# FIXME: does append not work?	=>	cat $install_tmplog >> $install_log
	cat "$install_log" "$install_tmplog" >"$install_log.new"
	mv "$install_log.new" "$install_log"

	# check exit code.
	if [ $ret -ne 0 ]; then
		echo
		echo $msg
		exit 1
	fi
}


function usage() {
	echo "Usage: $(basename $0) [options]"
	echo "Options:"
	echo "    --download-only    Only download software, do not build."
	echo "    --files=FILES      Directory with already downloaded files."
	echo "    --keep-files       Keeps downloaded files."
	echo "    --hadoop-only      Installs only Apache Hadoop."
	echo "    --hbase-only       Installs only Apache HBase."
	echo "    --help             Prints this help and exits."
	echo "    --no-config        Do not auto-configure Hadoop or HBase."
	echo "    --no-patches       Do not apply patches."
	echo "    --prefix=PREFIX    Changes installation prefix to PREFIX."
	echo "                       Defaults to /opt."
}


# parse arguments.
while [ $1 ]; do
	opt=$(echo $1 | sed 's/=.*//')
	arg=$(echo $1 | sed 's/.*=//')
	case $opt in
		"--download-only")
			download_only="true"
			;;
		"--files")
			files="$arg"
			keep_files="true" # do not delete files we did not download.
			;;
		"--hadoop-only")
			if [ $hbase_only ]; then
				echo "Error: --hbase-only and --hadoop-only used at the same time."
				usage
				exit 1
			fi
			hadoop_only="true"
			;;
		"--hbase-only")
			if [ $hadoop_only ]; then
				echo "Error: --hbase-only and --hadoop-only used at the same time."
				usage
				exit 1
			fi
			hbase_only="true"
			;;
		"--help")
			usage
			exit 0
			;;
		"--keep-files")
			keep_files="true"
			;;
		"--no-config")
			no_config="true"
			;;
		"--no-patches")
			no_patches="true"
			;;
		"--prefix")
			prefix="$arg"
			;;
		*)
			if [ ! "x" = "x$opt" ]; then
				echo "Unknown argument: $opt"
				usage
				exit 1
			fi
			;;
	esac
	shift
done


if [ "x" == "x$JAVA_HOME" ]; then
	echo "WARNING: \$JAVA_HOME is not set. This might cause trouble later on."
	echo
fi

# make sure the user knows what's up.
echo "this script will download, patch and install hadoop & hbase in $prefix"
echo "any key to continue, CTRL-C to abort."
read

if [ -f $prefix ]; then
	echo "$prefix is a file; can't install there."
	exit 1
fi

# create target directory.
if [ ! -d $prefix ]; then
	mkdir -p $prefix
	if [ $? != 0 ]; then
		echo "could not create directory $prefix"
		exit 1
	fi
fi

# truncate logs.
>"$install_log"
>"$install_log.new"


# check for necessary programs.
echo "Checking for necessary programs: ant and wget."
for command in "ant -version" "patch --version" "wget --version"; do
	program=$(echo $command | sed 's/ .*//')
	$command > /dev/null
	if [ $? -ne 0 ]; then
		echo "error: could not find $program"
		exit 1
	fi
done


# keep track of what tars we have.
tars=""

if [ "x" = "x$files" ]; then
	# download to some temporary directory.
	
	echo "Creating temporary directory."
	files=$(mktemp -d /tmp/hadoop-hbase-install.XXXXXX)
	mkdir -vp $files/patches


	cd $files
	echo "Downloading files."
	# printing progress to screen, without logging.
	# empty hadoop (?)
	if [ ! "x" = "x$hbase_only" ]; then
		echo "Skipping download of Apache Hadoop."
	else
		# hadoop tar
		exec_and_log "wget $hadoop_url" "Error: Could not download $hadoop_url" "true"
		tars="$tars $hadoop_tar"
		# patches.
		if [ ! "x" = "x$no_patches" ]; then
			echo "Will not patch Hadoop."
		else
			cd patches
			exec_and_log "wget $patch_1722_url" "Error: Could not download $patch_1722_url" "true"
			exec_and_log "wget $patch_5450_url" "Error: Could not download $patch_5450_url" "true"
			tars="$tars patches/$patch_1722 patches/$patch_5450"
		fi
	fi
	if [ ! "x" = "x$hadoop_only" ]; then
		echo "Skipping download of HBase."
	else
		cd $files
		# hbase tar
		exec_and_log "wget $hbase_url" "Error: Could not download $hbase_url" "true"
		tars="$tars $hbase_tar"
	fi
	echo "Done downloading. You will find the files in $files."
else
	for file in $tars; do
		exec_and_log "ls $files/$file" "Error: Could not find file $files/$file."
	done
	echo "Using previously downloaded files in $files"
fi


# stop if --download-only was supplied.
if [ "$download_only" = "true" ]; then
	echo "Download only: files were downloaded to $files."
	exit 0
fi

# install.
echo; echo "Installing."

# TODO: we *need* $JAVA_HOME to be correct.

# set default paths.
hadoop_home="$prefix/$hadoop_version"
hbase_home="$prefix/$hbase_version"
hadoop_conf=$hadoop_home/conf
hbase_conf=$hbase_home/conf

streaming_src="$hadoop_home/src/contrib/streaming"
streaming_target="$hadoop_home/build"



# hadoop
if [ ! "x" = "x$hbase_only" ]; then
	echo "Skipping installation of Apache Hadoop."
else
	echo "Extracting Hadoop to $prefix"
	exec_and_log "tar zxf $files/$hadoop_tar -C $prefix"
	echo "done."

	cd $hadoop_home

	if [ ! "x" = "x$no_patches" ]; then
		echo "Not patching Hadoop."
	else
		echo "Patching Hadoop."
		for patch in "$patch_1722" "$patch_5450"; do
			echo "Applying patch $patch"

			# inlined exec_and_log because of sh -c "command".
			# execute and log to intermediate.
			sh -c "patch -p0 <$files/patches/$patch | tee '$install_tmplog' | cat"
			ret=$?

			# log.
			cat "$install_log" "$install_tmplog" >"$install_log.new"
			mv "$install_log.new" "$install_log"
 
			# check exit code.
			if [ $ret -ne 0 ]; then
				echo
				echo "Error: Could not apply patch $patch."
				exit 1
			fi
		done
		echo "done."
		
		echo "Compiling Hadoop (logging to $install_log)."
		exec_and_log "ant" "Error: Could not compile Hadoop."
		echo "done."

		echo "Compiling Hadoop Streaming."
		echo "cd ${streaming_src}"
		echo "where I'll"
		echo "ant -Dversion=${version} -Ddist.dir=${streaming_target} package"
		cd ${streaming_src} ; echo pwd;  ant -Dversion=${version} -Ddist.dir=${streaming_target} package
		echo "done."
	fi
fi

# hbase.
if [ ! "x" = "x$hadoop_only" ]; then
	echo "Skipping installation of HBase."
else
	echo "Extracting HBase to $prefix."
	exec_and_log "tar zxf $files/$hbase_tar -C $prefix"
	echo "done."

	cd $hbase_home
	echo "Compiling HBase (logging to $install_log)."
	exec_and_log "ant" "Error: Could not compile Apache HBase."
	echo "done."
fi


# configuration?
if [ "x" = "x$no_config" ]; then
	if [ "x" = "x$hbase_only" ]; then
		echo "Configuring Hadoop."
		# backup template configurations.
		exec_and_log "cp -v $hadoop_conf/hadoop-env.sh $hadoop_conf/hadoop-env.sh.dist"
		exec_and_log "cp -v $hadoop_conf/core-site.xml $hadoop_conf/core-site.xml.dist"
		exec_and_log "cp -v $hadoop_conf/hdfs-site.xml $hadoop_conf/hdfs-site.xml.dist"
		exec_and_log "cp -v $hadoop_conf/mapred-site.xml $hadoop_conf/mapred-site.xml.dist"

		# emit configuration.
		cat << EOHADOOPENV > $hadoop_conf/hadoop-env.sh
# Set Hadoop-specific environment variables here.

# The only required environment variable is JAVA_HOME.  All others are
# optional.  When running a distributed configuration it is best to
# set JAVA_HOME in this file, so that it is correctly defined on
# remote nodes.

# The java implementation to use.  Required.
# export JAVA_HOME=/usr/lib/jvm/java-6-sun
# Debian Magic:
export JAVA_HOME=\`ls -l /etc/alternatives/java | sed 's#.* -> \(.*\)/jre/bin/java#\1#'\`

# Extra Java CLASSPATH elements.  Optional.
# export HADOOP_CLASSPATH=

# The maximum amount of heap to use, in MB. Default is 1000.
# export HADOOP_HEAPSIZE=2000

# Extra Java runtime options.  Empty by default.
# export HADOOP_OPTS=-server

# Command specific options appended to HADOOP_OPTS when specified
export HADOOP_NAMENODE_OPTS="-Dcom.sun.management.jmxremote $HADOOP_NAMENODE_OPTS"
export HADOOP_SECONDARYNAMENODE_OPTS="-Dcom.sun.management.jmxremote $HADOOP_SECONDARYNAMENODE_OPTS"
export HADOOP_DATANODE_OPTS="-Dcom.sun.management.jmxremote $HADOOP_DATANODE_OPTS"
export HADOOP_BALANCER_OPTS="-Dcom.sun.management.jmxremote $HADOOP_BALANCER_OPTS"
export HADOOP_JOBTRACKER_OPTS="-Dcom.sun.management.jmxremote $HADOOP_JOBTRACKER_OPTS"
# export HADOOP_TASKTRACKER_OPTS=
# The following applies to multiple commands (fs, dfs, fsck, distcp etc)
# export HADOOP_CLIENT_OPTS

# Extra ssh options.  Empty by default.
# export HADOOP_SSH_OPTS="-o ConnectTimeout=1 -o SendEnv=HADOOP_CONF_DIR"

# Where log files are stored.  $HADOOP_HOME/logs by default.
# export HADOOP_LOG_DIR=${HADOOP_HOME}/logs

# File naming remote slave hosts.  $HADOOP_HOME/conf/slaves by default.
# export HADOOP_SLAVES=${HADOOP_HOME}/conf/slaves

# host:path where hadoop code should be rsync'd from.  Unset by default.
# export HADOOP_MASTER=master:/home/$USER/src/hadoop

# Seconds to sleep between slave commands.  Unset by default.  This
# can be useful in large clusters, where, e.g., slave rsyncs can
# otherwise arrive faster than the master can service them.
# export HADOOP_SLAVE_SLEEP=0.1

# The directory where pid files are stored. /tmp by default.
# export HADOOP_PID_DIR=/var/hadoop/pids

# A string representing this instance of hadoop. $USER by default.
# export HADOOP_IDENT_STRING=$USER

# The scheduling priority for daemon processes.  See 'man nice'.
# export HADOOP_NICENESS=10
EOHADOOPENV

		cat <<CORESITE > $hadoop_conf/core-site.xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
  <property>
	<name>fs.default.name</name>
	<value>hdfs://localhost:9000</value>
  </property>
</configuration>
CORESITE

		cat <<HDFSSITE > $hadoop_conf/hdfs-site.xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
  <property>
	<name>fs.default.name</name>
	<value>hdfs://localhost:9000</value>
  </property>
  <property>
	<name>dfs.replication</name>
	<value>1</value>
  </property>
  <property>
    <name>dfs.datanode.socket.write.timeout</name>
    <value>0</value>
  </property>
</configuration>
HDFSSITE
		cat <<MAPREDSITE > $hadoop_conf/mapred-site.xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
  <property>
	<name>fs.default.name</name>
	<value>hdfs://localhost:9000</value>
  </property>
  <property>
	<name>mapred.job.tracker</name>
	<value>localhost:9001</value>
  </property>
</configuration>
MAPREDSITE

		echo "done."
	fi
	if [ "x" = "x$hadoop_only" ]; then
	    # TODO: set hbase.rootdir = hdfs://localhost:9000/hbase
		echo "Configuring HBase."
		# backup template configuration.
		exec_and_log "cp -v $hbase_conf/hbase-env.sh $hbase_conf/hbase-env.sh.dist"
		exec_and_log "cp -v $hbase_conf/hbase-site.xml $hbase_conf/hbase-site.xml.dist"

		# emit configuration.
		cat <<EOHBASEENV >$hbase_conf/hbase-env.sh
# Set environment variables here.

# The java implementation to use.  Java 1.6 required.
# export JAVA_HOME=/usr/java/jdk1.6.0/
# Debian Magic
export JAVA_HOME=\`ls -l /etc/alternatives/java | sed 's#.* -> \(.*\)/jre/bin/java#\1#'\`

# Extra Java CLASSPATH elements.  Optional.
# export HBASE_CLASSPATH=

# The maximum amount of heap to use, in MB. Default is 1000.
export HBASE_HEAPSIZE=3000

# Extra Java runtime options.
# Below are what we set by default.  May only work with SUN JVM.
# For more on why as well as other possible settings,
# see http://wiki.apache.org/hadoop/PerformanceTuning
export HBASE_OPTS="-XX:+HeapDumpOnOutOfMemoryError -XX:+UseConcMarkSweepGC -XX:+CMSIncrementalMode"

# Extra Java runtime options.  Empty by default.
# export HBASE_OPTS=-server

# File naming hosts on which HRegionServers will run.  $HBASE_HOME/conf/regionservers by default.
# export HBASE_REGIONSERVERS=${HBASE_HOME}/conf/regionservers

# Extra ssh options.  Empty by default.
# export HBASE_SSH_OPTS="-o ConnectTimeout=1 -o SendEnv=HBASE_CONF_DIR"

# Where log files are stored.  $HBASE_HOME/logs by default.
# export HBASE_LOG_DIR=${HBASE_HOME}/logs

# A string representing this instance of hbase. $USER by default.
# export HBASE_IDENT_STRING=$USER

# The scheduling priority for daemon processes.  See 'man nice'.
# export HBASE_NICENESS=10

# The directory where pid files are stored. /tmp by default.
# export HBASE_PID_DIR=/var/hadoop/pids

# Seconds to sleep between slave commands.  Unset by default.  This
# can be useful in large clusters, where, e.g., slave rsyncs can
# otherwise arrive faster than the master can service them.
# export HBASE_SLAVE_SLEEP=0.1

# export HBASE_MANAGES_ZK=true
EOHBASEENV

		cat <<EOF > $hbase_conf/hbase-site.xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>hbase.master.port</name>
    <value>60000</value>
    <description>The port master should bind to.</description>
  </property>

  <property>
    <name>hbase.cluster.distributed</name>
    <value>false</value>
    <description>The mode the cluster will be in. Possible values are
      false: standalone and pseudo-distributed setups with managed Zookeeper
      true: fully-distributed with unmanaged Zookeeper Quorum (see hbase-env.sh)
    </description>
  </property>

  <property>
    <name>hbase.rootdir</name>
    <value>hdfs://localhost:9000/hbase</value>
    <description>The directory shared by region servers.
    </description>
  </property>
</configuration>
EOF

		echo "done."
	fi
else
	echo "Auto-configuration disabled."
	echo "Edit the following files to configure Hadoop and HBase:"
	echo "* $hadoop_conf/hadoop-env.sh"
	echo "* $hadoop_conf/hadoop-site.xml"
	echo "* $hbase_conf/hbase-env.sh"
fi

# change ownership of installation directories.
if [ "empty" != "empty$SUDO_UID" ]; then 
	# we're sudoing. let's go!
	echo "chowning $hadoop_home and $hbase_home to user id $SUDO_UID"
	chown -R $SUDO_UID $hadoop_home $hbase_home
fi

# clean up.
if [ "x" = "x$keep_files" ]; then
	echo "removing $files"
	rm -rf $files # not using exec_and_log for a reason.
else
	echo "(keeping files in $files)"
fi

echo "removing $install_tmplog."
rm $install_tmplog


# print further instructions.
echo "

Congratulations!

Hadoop and HBase are installed in $prefix
I'll leave it to you to start hadoop and hbase.

You need to perform these steps:

 (setup passphraseless ssh)
 format namenode
 start hadoop & hbase & thrift

Which is something like this in pseudo-bash:

  # format namenode.
  $hadoop_home/bin/hadoop namenode -format	# look twice!
  # start hadoop.
  $hadoop_home/bin/start-all.sh
  # start hbase.
  $hbase_home/bin/start-hbase.sh
  # start hbase's thrift server.
  $hbase_home/bin/hbase thrift start

You will find help at http://hadoop.apache.org/core/docs/current/quickstart.html
and http://wiki.apache.org/hadoop/Hbase/10Minutes

Thank you, it's been fun automating things for you!
"
