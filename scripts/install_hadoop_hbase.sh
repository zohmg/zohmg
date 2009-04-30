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
install_log="$(pwd)/hadoop_hbase_install.log"
install_tmplog=$(mktemp /tmp/zohmg-log.XXXXXXXX)


# helpers.

# execute $1 and exit if it failed, displaying $2.
# it is possible to set $3 in order to print to screen (without logging).
function exec_and_log() {
    # setup variables.
    command=$1
    [ "x" = "x$2" ] && msg="Error: Could not execute $command." || msg=$2
    screenoutput=$3

    # execute and log to intermediate.
    if [ "x" = "x$screenoutput" ]; then
        $1 &>$install_tmplog
    else
        $1
    fi
    ret=$?

    # log if not requested not to.
    if [ "x" = "x$3" ]; then
        cat $install_log $install_tmplog >"$install_log.new"
        mv "$install_log.new" $install_log
    fi

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


# truncate logs.
>$install_log
>"$install_log.new"


# set default paths.
[ "x" = "x$hadoop" ] && hadoop="$prefix/hadoop"
[ "x" = "x$hbase" ] && hbase="$prefix/hbase"


# check for necessary programs.
echo "Checking for necessary programs..."
for command in "ant -version" "patch --version" "wget --version"; do
    program=$(echo $command | sed 's/ .*//')
    printf "Checking for $program... "
    exec_and_log "$command" "Error: Missing program: $program not found."
    echo "ok."
done


# download or use already existing files.
if [ "x" = "x$files" ]; then
    # create temporary directories for downloads.
    printf "Creating temporary directory... "
    files=$(mktemp -d /tmp/zohmg-deps.XXXXXX)
    mkdir -p $files/patches
    echo "done."
    echo "Downloading files... "
    # printing progress to screen, without logging.
    # release files.
    cd $files
    exec_and_log "wget $hadoop_release" "Error: Could not download $hadoop_release" "true"
    exec_and_log "wget $hbase_release" "Error: Could not download $hbase_release" "true"
    # download patches.
    cd patches
    exec_and_log "wget $hadoop_1722" "Error: Could not download $hadoop_1722" "true"
    exec_and_log "wget $hadoop_5450" "Error: Could not download $hadoop_5450" "true"
    echo "Done downloading files."
else
    printf "Using previously downloaded files in $files... "
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

# check permissions.
for dir in "$hadoop" "$hbase"; do
    exec_and_log "mkdir -p $dir" "Error: Could not create $dir."
done

# hadoop
if [ ! "x" = "x$hbase_only" ]; then
    echo "Skipping installation of Apache Hadoop..."
else
    printf "Extracting Apache Hadoop... "
    exec_and_log "mkdir -p $hadoop"
    exec_and_log "tar zxf $files/$hadoop_tar -C $hadoop"
    echo "done."
    for patch in "$patch_1722" "$patch_5450"; do
        num=$(echo $patch | sed 's/.patch$//')
        printf "Applying patch $num... "
        exec_and_log "cd $hadoop/$hadoop_version ; patch -p0 <$files/patches/$patch" "Error: Could not apply patch $num."
        echo "done."
    done
    printf "Compiling Apache Hadoop... "
    exec_and_log "echo ... Compiling Apache Hadoop ..."
    exec_and_log "ant package" "Error: Could not compile Apache Hadoop."
    echo "done."
fi

# hbase.
if [ ! "x" = "x$hadoop_only" ]; then
    echo "Skipping installation of Apache HBase..."
else
    printf "Extracting Apache HBase... "
    exec_and_log "mkdir -p $hbase"
    exec_and_log "tar zxf $files/$hbase_tar -C $hbase"
    echo "done."
    exec_and_log "cd $hbase/$hbase_version"
    printf "Compiling Apache HBase... "
    exec_and_log "echo ... Compiling Apache HBase ..."
    exec_and_log "ant package" "Error: Could not compile Apache HBase."
    echo "done."
fi


# configuration?
if [ "x" = "x$no_config" ]; then
    if [ "x" = "x$hbase_only" ]; then
        printf "Configuring Apache Hadoop... "
        cd $hadoop/$hadoop_version/conf
        exec_and_log "cp -v hadoop-env.sh hadoop-env.sh.dist"
        exec_and_log "cp -v hadoop-site.xml hadoop-site.xml.dist"
        exec_and_log "cp -v $files/conf/hadoop-env.sh ."
        exec_and_log "cp -v $files/conf/hadoop-site.xml ."
        echo "done."
    fi
    if [ "x" = "x$hadoop_only" ]; then
        printf "Configuring Apache HBase... "
        cd $hbase/$hbase_version/conf
        exec_and_log "cp -v hbase-env.sh hbase-env.sh.dist"
        exec_and_log "cp -v $files/conf/hbase-env.sh ."
        echo "done."
    fi
else
    echo "Edit the following files to configure Hadoop and HBase:"
    echo "* $hadoop/$hadoop_version/conf/hadoop-env.sh"
    echo "* $hadoop/$hadoop_version/conf/hadoop-site.xml"
    echo "* $hbase/$hbase_version/conf/hbase-env.sh"
fi


# clean up.
rm "$install_log.new"
rm $install_tmplog
if [ "x" = "x$keep_files" ]; then
    printf "Cleaning up downloaded files... "
    exec_and_log "rm -rf $files" "Error: Could not remove $files."
    echo "done."
else
    echo "Not cleaning up downloaded files in $files."
fi


echo "Done."
