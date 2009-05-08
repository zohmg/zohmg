#!/bin/sh


if [ $EUID -ne 0 ]; then
    echo "Error: Superuser privileges required."
    exit 1
fi


# set default variables.
prefix="/opt"
hadoop_version="hadoop-0.19.1"
hadoop_tar="$hadoop_version.tar.gz"
patch_1722="HADOOP-1722-branch-0.19.patch"
patch_5450="HADOOP-5450.patch"
hbase_version="hbase-0.19.1"
hbase_tar="$hbase_version.tar.gz"
hadoop_release="http://mirrors.ukfast.co.uk/sites/ftp.apache.org/hadoop/core/hadoop-0.19.1/$hadoop_tar"
hadoop_1722="https://issues.apache.org/jira/secure/attachment/12401426/$patch_1722"
hadoop_5450="https://issues.apache.org/jira/secure/attachment/12401846/$patch_5450"
hbase_release="http://mirrors.ukfast.co.uk/sites/ftp.apache.org/hadoop/hbase/hbase-0.19.1/$hbase_tar"
install_log="$(pwd)/install_hadoop_hbase.log"
install_tmplog=$(mktemp /tmp/zohmg-log.XXXXXXXX)


# helpers.

# execute $1 and exit if it failed, displaying $2.
function exec_and_log() {
    # setup variables.
    command=$1
    [ "x" = "x$2" ] && msg="Error: Could not execute $command." || msg=$2

    # execute and log to intermediate.
    $1 | tee "$install_tmplog" | cat
    ret=$?

    # log.
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
    echo "    --download-only      Only download software, do not build."
    echo "    --files=FILES        Directory with already downloaded files."
    echo "                         Files are downloaded to /tmp/zohmg-deps.XXXXXX."
    echo "    --hadoop-only        Installs only Apache Hadoop."
    echo "                         Cannot be used with --hbase-only."
    echo "    --hbase-only         Installs only Apache HBase."
    echo "                         Cannot be used with --hadoop-only."
    echo "    --help               Prints this help and exits."
    echo "    --keep-files         Keeps downloaded files."
    echo "    --no-config          Do not configure Hadoop or HBase."
    echo "    --prefix=PREFIX      Changes installation prefix to PREFIX."
    echo "                         Defaults to /opt."
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


# truncate logs.
>"$install_log"
>"$install_log.new"


# set default paths.
hadoop="$prefix/$hadoop_version"
hbase="$prefix/$hbase_version"
hadoop_conf=$hadoop/conf
hbase_conf=$hbase/conf


# check for necessary programs.
echo "Checking for necessary programs..."
for command in "ant -version" "patch --version" "wget --version"; do
    program=$(echo $command | sed 's/ .*//')
    echo "Checking for $program... "
    exec_and_log "$command" "Error: Missing program: $program not found."
    echo "ok."
done


# download or use already existing files.
if [ "x" = "x$files" ]; then
    # create temporary directories for downloads.
    echo "Creating temporary directory... "
    files=$(mktemp -d /tmp/zohmg-deps.XXXXXX)
    mkdir -p $files/patches
    echo "done."
    echo "Downloading files... "
    # printing progress to screen, without logging.
    cd $files
    # empty hadoop
    if [ ! "x" = "x$hbase_only" ]; then
        echo "Skipping download of Apache Hadoop..."
    else
        # hadoop release file.
        exec_and_log "wget $hadoop_release" "Error: Could not download $hadoop_release" "true"
        # download patches.
        cd patches
        exec_and_log "wget $hadoop_1722" "Error: Could not download $hadoop_1722" "true"
        exec_and_log "wget $hadoop_5450" "Error: Could not download $hadoop_5450" "true"
    fi
    if [ ! "x" = "x$hadoop_only" ]; then
        echo "Skipping download of Apache HBase..."
    else
        cd $files
        # hbase release file.
        exec_and_log "wget $hbase_release" "Error: Could not download $hbase_release" "true"
    fi
    echo "Done downloading files."
else
    echo "Using previously downloaded files in $files... "
    for file in "patches/$patch_1722" "patches/$patch_5450" "$hadoop_tar" "$hbase_tar"; do
        exec_and_log "ls $files/$file" "Error: Could not find file $files/$file."
    done
    echo "ok."
fi


# stop if --download-only was supplied.
if [ "$download_only" = "true" ]; then
    echo "Files downloaded to $files ."
    exit 0
fi


# install.
echo "Installing..."

# hadoop
if [ ! "x" = "x$hbase_only" ]; then
    echo "Skipping installation of Apache Hadoop..."
else
    echo "Extracting Apache Hadoop... "
    exec_and_log "tar zxf $files/$hadoop_tar -C $prefix"
    echo "done."
    exec_and_log "echo ... Patching Apache Hadoop ..."
    for patch in "$patch_1722" "$patch_5450"; do
        num=$(echo $patch | sed 's/.patch$//')
        echo "Applying patch $num... "
        cd $hadoop
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
            echo "Error: Could not apply patch $num."
            exit 1
        fi
        echo "done."
    done
    exec_and_log "echo ok"
    echo "Compiling Apache Hadoop... "
    exec_and_log "echo ... Compiling Apache Hadoop ..."
    cd $hadoop
    exec_and_log "ant package" "Error: Could not compile Apache Hadoop."
    echo "done."
fi

# hbase.
if [ ! "x" = "x$hadoop_only" ]; then
    echo "Skipping installation of Apache HBase..."
else
    echo "Extracting Apache HBase... "
    exec_and_log "tar zxf $files/$hbase_tar -C $prefix"
    echo "done."
    echo "Compiling Apache HBase... "
    exec_and_log "echo ... Compiling Apache HBase ..."
    cd $hbase
    exec_and_log "ant package" "Error: Could not compile Apache HBase."
    echo "done."
fi


# configuration?
if [ "x" = "x$no_config" ]; then
    if [ "x" = "x$hbase_only" ]; then
        echo "Configuring Apache Hadoop... "
        # backup template configurations.
        exec_and_log "cp -v $hadoop_conf/hadoop-env.sh $hadoop_conf/hadoop-env.sh.dist"
        exec_and_log "cp -v $hadoop_conf/hadoop-site.xml $hadoop_conf/hadoop-site.xml.dist"

        # emit configuration.
        cat << EOHADOOPENV >$hadoop_conf/hadoop-env.sh
# Set Hadoop-specific environment variables here.

# The only required environment variable is JAVA_HOME.  All others are
# optional.  When running a distributed configuration it is best to
# set JAVA_HOME in this file, so that it is correctly defined on
# remote nodes.

# The java implementation to use.  Required.
# export JAVA_HOME=/usr/lib/j2sdk1.5-sun
# Automatically infer \$JAVA_HOME on Debian based systems.
export JAVA_HOME=\`ls -l /etc/alternatives/java | sed 's#.* -> \(.*\)/jre/bin/java#\1#'\`

# Extra Java CLASSPATH elements.  Optional.
# export HADOOP_CLASSPATH=

# The maximum amount of heap to use, in MB. Default is 1000.
# export HADOOP_HEAPSIZE=2000

# Extra Java runtime options.  Empty by default.
# export HADOOP_OPTS=-server

# Command specific options appended to HADOOP_OPTS when specified
export HADOOP_NAMENODE_OPTS="-Dcom.sun.management.jmxremote \$HADOOP_NAMENODE_OPTS"
export HADOOP_SECONDARYNAMENODE_OPTS="-Dcom.sun.management.jmxremote \$HADOOP_SECONDARYNAMENODE_OPTS"
export HADOOP_DATANODE_OPTS="-Dcom.sun.management.jmxremote \$HADOOP_DATANODE_OPTS"
export HADOOP_BALANCER_OPTS="-Dcom.sun.management.jmxremote \$HADOOP_BALANCER_OPTS"
export HADOOP_JOBTRACKER_OPTS="-Dcom.sun.management.jmxremote \$HADOOP_JOBTRACKER_OPTS"
# export HADOOP_TASKTRACKER_OPTS=
# The following applies to multiple commands (fs, dfs, fsck, distcp etc)
# export HADOOP_CLIENT_OPTS

# Extra ssh options.  Empty by default.
# export HADOOP_SSH_OPTS="-o ConnectTimeout=1 -o SendEnv=HADOOP_CONF_DIR"

# Where log files are stored.  \$HADOOP_HOME/logs by default.
# export HADOOP_LOG_DIR=\${HADOOP_HOME}/logs

# File naming remote slave hosts.  \$HADOOP_HOME/conf/slaves by default.
# export HADOOP_SLAVES=\${HADOOP_HOME}/conf/slaves

# host:path where hadoop code should be rsync'd from.  Unset by default.
# export HADOOP_MASTER=master:/home/\$USER/src/hadoop

# Seconds to sleep between slave commands.  Unset by default.  This
# can be useful in large clusters, where, e.g., slave rsyncs can
# otherwise arrive faster than the master can service them.
# export HADOOP_SLAVE_SLEEP=0.1

# The directory where pid files are stored. /tmp by default.
# export HADOOP_PID_DIR=/var/hadoop/pids

# A string representing this instance of hadoop. \$USER by default.
# export HADOOP_IDENT_STRING=\$USER

# The scheduling priority for daemon processes.  See 'man nice'.
# export HADOOP_NICENESS=10
EOHADOOPENV
        cat <<EOHADOOPSITE >$hadoop_conf/hadoop-site.xml
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
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
</configuration>
EOHADOOPSITE
        echo "done."
    fi
    if [ "x" = "x$hadoop_only" ]; then
        echo "Configuring Apache HBase... "
        # backup template configuration.
        exec_and_log "cp -v $hbase_conf/hbase-env.sh $hbase_conf/hbase-env.sh.dist"

        # emit configuration.
        cat <<EOHBASEENV >$hbase_conf/hbase-env.sh
#
#/**
# * Copyright 2007 The Apache Software Foundation
# *
# * Licensed to the Apache Software Foundation (ASF) under one
# * or more contributor license agreements.  See the NOTICE file
# * distributed with this work for additional information
# * regarding copyright ownership.  The ASF licenses this file
# * to you under the Apache License, Version 2.0 (the
# * "License"); you may not use this file except in compliance
# * with the License.  You may obtain a copy of the License at
# *
# *     http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# */

# Set environment variables here.

# The java implementation to use.  Java 1.6 required.
# export JAVA_HOME=/usr/java/jdk1.6.0/
# Automatically infer \$JAVA_HOME on Debian based systems.
export JAVA_HOME=\`ls -l /etc/alternatives/java | sed 's#.* -> \(.*\)/jre/bin/java#\1#'\`

# Extra Java CLASSPATH elements.  Optional.
# export HBASE_CLASSPATH=

# The maximum amount of heap to use, in MB. Default is 1000.
# export HBASE_HEAPSIZE=1000

# Extra Java runtime options.  Empty by default.
# export HBASE_OPTS=-server

# File naming hosts on which HRegionServers will run.  \$HBASE_HOME/conf/regionservers by default.
# export HBASE_REGIONSERVERS=\${HBASE_HOME}/conf/regionservers

# Extra ssh options.  Empty by default.
# export HBASE_SSH_OPTS="-o ConnectTimeout=1 -o SendEnv=HBASE_CONF_DIR"

# Where log files are stored.  \$HBASE_HOME/logs by default.
# export HBASE_LOG_DIR=\${HBASE_HOME}/logs

# A string representing this instance of hbase. \$USER by default.
# export HBASE_IDENT_STRING=\$USER

# The scheduling priority for daemon processes.  See 'man nice'.
# export HBASE_NICENESS=10

# The directory where pid files are stored. /tmp by default.
# export HBASE_PID_DIR=/var/hadoop/pids

# Seconds to sleep between slave commands.  Unset by default.  This
# can be useful in large clusters, where, e.g., slave rsyncs can
# otherwise arrive faster than the master can service them.
# export HBASE_SLAVE_SLEEP=0.1
EOHBASEENV
        echo "done."
    fi
else
    echo "Edit the following files to configure Hadoop and HBase:"
    echo "* $hadoop_conf/hadoop-env.sh"
    echo "* $hadoop_conf/hadoop-site.xml"
    echo "* $hbase_conf/hbase-env.sh"
fi


# clean up.
rm $install_tmplog
if [ "x" = "x$keep_files" ]; then
    echo "Cleaning up downloaded files... "
    exec_and_log "rm -rf $files" "Error: Could not remove $files."
    echo "done."
else
    echo "Not cleaning up files in $files."
fi


echo "Done."
