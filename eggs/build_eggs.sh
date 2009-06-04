#!/bin/sh

cd `dirname $0`

mkdir build 2> /dev/null
for setup in `ls setup-*.py`; do
	python $setup bdist_egg >> build/setup.log
	# TODO: check $? 
done
echo "eggs shelled - please check build/setup.log if you're feeling inquisitive."
