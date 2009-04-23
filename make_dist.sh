#!/bin/sh

set -e

# TODO: get version from somewhere
DATE=$(date +%Y%m%d)
GITCOMMIT="git$(git log -1 | sed -n '/commit/ {s/commit //;p}')"
VERSION="alpha-$DATE-$GITCOMMIT"
BUILD=zohmg-$VERSION
DIST=dist
BUILD_TARGET=$DIST/$BUILD

printf "Creating dist target..."
mkdir -p $BUILD_TARGET
echo "done."

printf "Copying dist files to temporary target..."
cp AUTHORS INSTALL QUICKSTART README TODO $BUILD_TARGET
cp install.py setup.py $BUILD_TARGET
cp -r examples java lib src tests zohmg $BUILD_TARGET
echo "done."

printf "Creating dist tar archive..."
cd $DIST
tar -zcf $BUILD.tar.gz $BUILD
echo "done."

printf "Cleaning temporary files..."
rm -r $BUILD
echo "done."
