#!/bin/sh

echo "installing eggs with easy_install"

oldpp=$PYTHONPATH
for egg in `ls dist/*.egg`; do
    echo "installing $egg"
    PYTHONPATH="$1" sudo easy_install -zax $egg
done
export PYTHONPATH=oldpp

echo
