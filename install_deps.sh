#!/bin/sh

# outline
# - set default options
# - parse options
# - check for programs needed
# - for each sw
#   - download
#   - maybe patch
#   - maybe ant package


# helpers.
function usage() {
    echo "Usage: $(basename $0) [options]"
    echo "Options:"
    echo "    --download-only      Only download software, do not build."
    echo "    --hadoop-dir=HADOOP  Changes Apache Hadoop installation dir to HADOOP."
    echo "    --hbase-dir=HBASE    Changes Apache HBase installation dir to HBASE."
    echo "    --hadoop-only        Installs only Apache Hadoop."
    echo "                         Cannot be used with --hbase-only."
    echo "    --hbase-only         Installs only Apache HBase."
    echo "                         Cannot be used with --hadoop-only."
    echo "    --help               Prints this help and exits."
    echo "    --prefix=PREFIX      Changes installation prefix to PREFIX."
    echo "                         Defaults to /opt."
}


# set default variables.
PREFIX="/opt"
HADOOP_RELEASE="http://mirrors.ukfast.co.uk/sites/ftp.apache.org/hadoop/core/hadoop-0.19.1/hadoop-0.19.1.tar.gz"
HADOOP_1722="https://issues.apache.org/jira/secure/attachment/12401426/HADOOP-1722-branch-0.19.patch"
HADOOP_5450="https://issues.apache.org/jira/secure/attachment/12401846/HADOOP-5450.patch"
HBASE_RELEASE="http://mirrors.ukfast.co.uk/sites/ftp.apache.org/hadoop/hbase/hbase-0.19.1/hbase-0.19.1.tar.gz"


# parse arguments.
while [ $1 ]; do
    OPT=$(echo $1 | sed 's/=.*//')
    ARG=$(echo $1 | sed 's/.*=//')
    case $OPT in
        "--download-only")
            DOWNLOAD_ONLY=true
            ;;
        "--hadoop-only")
            if [ $HBASE_ONLY ]; then
                echo "Error: --hbase-only and --hadoop-only used at the same time."
                usage
                exit 1
            fi
            HADOOP_ONLY=true
            ;;
        "--hbase-only")
            if [ $HADOOP_ONLY ]; then
                echo "Error: --hbase-only and --hadoop-only used at the same time."
                usage
                exit 1
            fi
            HBASE_ONLY=true
            ;;
        "--hadoop-dir")
            HADOOP="$ARG"
            ;;
        "--hbase-dir")
            HBASE="$ARG"
            ;;
        "--help")
            usage
            exit 0
            ;;
        "--prefix")
            PREFIX="$ARG"
            ;;
        *)
            if [ ! "x" = "x$OPT" ]; then
                echo "Unknown argument: $OPT"
                usage
                exit 1
            fi
            ;;
    esac
    shift
done


# set paths.
[ "x" = "x$HADOOP" ] && HADOOP="$PREFIX/hadoop"
[ "x" = "x$HBASE" ] && HBASE="$PREFIX/hbase"


# check for needed software.
patch --version &>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: Missing program: patch not found."
    exit 1
fi
ant -version &>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: Missing program: ant not found."
    exit 1
fi


# create temporary directory for downloads.


# install
