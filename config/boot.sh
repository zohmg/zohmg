#!/usr/bin/bash


confdir=`dirname $0`
cd "$confdir/../lib"
zohmglibpath=`pwd`

echo adding \'$zohmglibpath\' to DOLLAR-PYTHONPATH.
export PYTHONPATH="$PYTHONPATH:$zohmglibpath"
