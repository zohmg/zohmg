#!/bin/sh

# clean,
sudo rm -rfv /usr/local/share/zohmg
sudo rm -rfv /usr/local/lib/zohmg
sudo rm -v /usr/bin/zohmg /usr/lib/python2.5/site-packages/zohmg-*-py2.5.egg /usr/lib/python2.5/site-packages/hbase-*-py2.5.egg /usr/lib/python2.5/site-packages/thrift-*-py2.5.egg
# HEY!: vi ska vara grymt forsiktiga med att ta bort egg som kan vara installerade sedan tidigare.

# reinstate.
echo -n hmm..
sudo python install.py > tmp/last.reinstall.log
sudo rm -rf build dist zohmg.egg-info
echo ok.
