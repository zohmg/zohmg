#!/bin/sh

# clean,
sudo rm -v /usr/bin/zohmg /usr/lib/python2.5/site-packages/zohmg-*-py2.5.egg /usr/lib/python2.5/site-packages/hbase-*-py2.5.egg /usr/lib/python2.5/site-packages/thrift-*-py2.5.egg

# reinstate.
echo -n hmm..
sudo python install.py  --verbose install > tmp/last.reinstall.log
sudo rm -rf build dist zohmg.egg-info
echo ok.
