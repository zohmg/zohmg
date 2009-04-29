#!/bin/sh

# everything you need is right here.
# step into the groove
cd `dirname $0`

echo "LET'S DO THE EGG DANCE!"
sh build_eggs.sh
sh install_eggs.sh
sh clean_eggs.sh
# sorry, there is no uninstall :-(
