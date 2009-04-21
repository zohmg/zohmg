#!/usr/bin/env python
import os, sys

def install():
    build_darling = False
    target = '/usr/share/zohmg'

    # check for rootness.
    if os.geteuid() != 0:
        print "you need to be root. please sudo."
        return
    print "installing!"

    # mkdir.
    create_share_dir(target)

    # darling.
    if build_darling:
        build_darling(target)
    else:
        copy_bundled_darling(target)

    # thrift & hbase
    copy_bundled_thrift(target)
    copy_bunded_hbase(target)


def setup():
    print
    print "installing zohmg: python setup.py install"
    r = os.system('python setup.py install > tmp/zohmg-install.log')
    if r != 0:
        print "errors?!"
        print "try again, it could work the second (or third) time."
        sys.exit(r)
    os.system("egrep '(Installing|Copying) zohmg' tmp/zohmg-install.log")

def create_share_dir(dir):
    if not os.path.exists(dir):
        os.system('mkdir ' + dir)

# not used atm; user would have to specify classpath == jobbigt.
def build_darling(target):
    print 'building java hook-ups'
    r = os.system('cd java/darling; ant')
    if r != 0:
        # fail!
        print 'problems building darling!'
        print 'hey, I need to know where to find jars for hbase, hadoop and hadoop streaming.'
        print 'please add them to $CLASSPATH and try again.'
        sys.exit(r)
    os.system("cp -v java/darling/build/darling-.jar " + target)

def copy_bundled_darling(target):
    print "copying pre-built darling.jar"
    os.system("cp -v lib/darling-*.jar " + target)

# copies thrift egg.
def copy_bundled_thrift(target):
    print "copying bundled thrift egg"
    os.system("cp -v lib/thrift-*.egg " + target)
    os.system("cp -v lib/Hbase.thrift " + target)

# copies hbase egg.
def copy_bunded_hbase(target):
    print "copying bundled hbase egg"
    os.system("cp -v lib/hbase-*.egg " + target)


if __name__ == "__main__":

    install()
    setup()

    print
    print "ok, that should do it!"
    print "now try this:"
    print "$> zohmg help"
    print
