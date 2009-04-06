#!/bin/bash


confdir=`dirname $0`
cd "$confdir/../lib"
zohmglibpath=`pwd`

echo adding \'$zohmglibpath\' to DOLLAR-PYTHONPATH.

if [ -z $PYTHONPATH ]; then
    export PYTHONPATH=~/whoop/lib:$zohmglibpath
else
    export PYTHONPATH="$PYTHONPATH:~/whoop/lib:$zohmglibpath"
fi

