#!/bin/sh
sudo rm -v /usr/bin/zohmg /usr/lib/python2.5/site-packages/zohmg-*-py2.5.egg
sudo python setup.py  --verbose install
