#!/bin/sh

echo spring-clean for the may queen

cd `dirname $0`
rm -rf build dist *.egg-info 2> /dev/null
