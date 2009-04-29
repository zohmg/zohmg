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
    echo "    --files=FILES        Directory with already downloaded files."
    echo "                         Files are downloaded to /tmp/zohmg-deps.XXXXXX."
    echo "    --hadoop-dir=HADOOP  Changes Apache Hadoop installation dir to HADOOP."
    echo "                         This option overrides the --prefix option."
    echo "    --hbase-dir=HBASE    Changes Apache HBase installation dir to HBASE."
    echo "                         This option overrides the --prefix option."
    echo "    --hadoop-only        Installs only Apache Hadoop."
    echo "                         Cannot be used with --hbase-only."
    echo "    --hbase-only         Installs only Apache HBase."
    echo "                         Cannot be used with --hadoop-only."
    echo "    --help               Prints this help and exits."
    echo "    --keep-files         Keeps downloaded files."
    echo "    --no-configi         Do not configure Hadoop or HBase."
    echo "    --prefix=PREFIX      Changes installation prefix to PREFIX."
    echo "                         Defaults to /opt."
}


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
install_log="install.log"


# truncate install.log.
>$install_log


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
        "--hadoop-dir")
            hadoop="$arg"
            ;;
        "--hbase-dir")
            hbase="$arg"
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


# set paths.
[ "x" = "x$hadoop" ] && hadoop="$prefix/hadoop"
[ "x" = "x$hbase" ] && hbase="$prefix/hbase"


# check for necessary programs.
echo "Checking for necessary programs..."
for command in "ant -version" "patch --version" "wget --version"; do
    program=$(echo $command | sed 's/ .*//')
    printf "Checking for $program... "
    $command >>$install_log
    if [ $? -ne 0 ]; then
        echo "Error: Missing program: $program not found."
        exit 1
    fi
    echo "ok."
done


# download or use already existing files.
if [ "x" = "x$files" ]; then
    # create temporary directories for downloads.
    printf "Creating temporary directory... "
    files=$(mktemp -d /tmp/zohmg-deps.XXXXXX)
    mkdir -p $files/patches
    echo "done."
    printf "Downloading files... "
    # release files.
    cd $files
    wget $hadoop_release >>$install_log
    wget $hbase_release >>$install_log
    # download patches.
    cd patches
    wget $hadoop_1722 >>$install_log
    wget $hadoop_5450 >>$install_log
    echo "done."
else
    printf "Using previously downloaded files in $files... "
    for file in "patches/$patch_1722" "patches/$patch_5450" "$hadoop_tar" "$hbase_tar"; do
        ls $files/$file >>$install_log
        if [ $? -ne 0 ]; then
            echo
            echo "Error: Could not find file $files/$file."
            exit 1
        fi
    done
    echo "ok."
fi


# stop if --download-only was supplied.
if [ "$download_only" = "true" ]; then
    echo "Files downloaded to $tmpdir ."
    exit 0
fi


# install.
echo "Installing..."

# check permissions.
for dir in "$hadoop" "$hbase"; do
    mkdir -p "$dir"
    if [ $? -ne 0 ]; then
        echo "Error: Could not create $dir."
        exit 1
    fi
done

# hadoop
printf "Extracting Apache Hadoop... "
mkdir -p $hadoop
tar zxf $files/$hadoop_tar -C $hadoop
echo "done."
cd $hadoop/$hadoop_version
for patch in "$patch_1722" "$patch_5450"; do
    num=$(echo $patch | sed 's/.patch$//')
    printf "Applying patch $num... "
    patch -p0 <"$files/patches/$patch" >>$install_log
    if [ $? -ne 0 ]; then
        echo
        echo "Error: Could not apply patch $num."
        exit 1
    fi
    echo "done."
done
printf "Compiling Apache Hadoop... "
ant package >>$install_log
if [ $? -ne 0 ]; then
    echo
    echo "Error: Could not compile Apache Hadoop."
    exit 1
fi
echo "done."

# hbase.
printf "Extracting Apache HBase... "
mkdir -p $hbase
tar zxf $files/$hbase_tar -C $hbase
echo "done."
cd $hbase/$hbase_version
printf "Compiling Apache HBase... "
ant package >>$install_log
if [ $? -ne 0 ]; then
    echo
    echo "Error: Could not compile Apache HBase."
    exit 1
fi
echo "done."


# configuration?
if [ "x" = "x$no_config" ]; then
    printf "Configuring Hadoop and HBase... "
    cd $hadoop/$hadoop_version/conf
    cp -v hadoop-env.sh hadoop-env.sh.dist >>$install_log
    cp -v hadoop-site.xml hadoop-site.xml.dist >>$install_log
    cp -v $files/conf/hadoop-env.sh $hadoop/$hadoop_version/conf >>$install_log
    cp -v $files/conf/hadoop-site.xml $hadoop/$hadoop_version/conf >>$install_log
    cp -v hbase-env.sh hbase-env.sh.dist >>$tmp_log
    cp -v $files/conf/hbase-env.sh $hbase/$hbase_version/conf >>$install_log
    echo "done."
else
    echo "Edit the following files to configure Hadoop and HBase:"
    echo "* $hadoop/$hadoop_version/conf/hadoop-env.sh"
    echo "* $hadoop/$hadoop_version/conf/hadoop-site.xml"
    echo "* $hbase/$hbase_version/conf/hbase-env.sh"
fi


# clean up.
if [ "x" = "x$keep_files" ]; then
    printf "Cleaning up downloaded files... "
    rm -rf $files
    echo "done."
else
    echo "Not cleaning up downloaded files in $files."
fi


echo "Done."
