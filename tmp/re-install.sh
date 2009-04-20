#!/bin/sh

# clean,
sudo rm -v /usr/bin/zohmg /usr/lib/python2.5/site-packages/zohmg-*-py2.5.egg

# reinstate.
echo -n hmm..
sudo python setup.py  --verbose install > tmp/last.reinstall.log
echo ok.
