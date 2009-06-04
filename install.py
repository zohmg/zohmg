# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

#!/usr/bin/env python
import os, shutil, sys

# FHS-compliant.
share_target = '/usr/local/share/zohmg'
doc_target   = '/usr/local/share/zohmg/doc'
lib_target   = '/usr/local/lib/zohmg'


def clean():
    """cleans things a bit."""
    print
    print 'cleaning previous zohmg installation:'

    for dir in [share_target, doc_target, lib_target]:
        print "  " + dir
        os.system("rm -rf %s" % dir)


def copy_files():
    """populate /usr/local/lib/zohmg and /usr/local/share/zohmg"""
    print
    print "populating zohmg directories:"

    # create directories.
    for dir in [share_target, doc_target, lib_target]:
        if not os.path.isdir(dir):
            os.mkdir(dir)

    # copy docs.
    docs = ['README']
    for doc in docs:
        copy_file(doc, doc, doc_target)

    # copy stuff to share
    copy_file("bundled hbase thrift interface", "lib/Hbase.thrift", share_target)
    shutil.copytree("examples", share_target+"/examples")
    # and to lib
    shutil.copytree("zohmg/middleware", lib_target+"/middleware")
    shutil.copytree("static-skeleton", lib_target+"/static-skeleton")
    copy_file("pre-built python eggs", "lib/*.egg", lib_target)
    copy_file("pre-built darling jar", "lib/darling-*.jar", lib_target)
    copy_file("dumbo mapper import script","lib/import.py", lib_target)


# assumes that setuptools is available.
def python_modules():
    print
    print "building python eggs:"

    egg_target = lib_target
    egg_log = '/tmp/zohmg-egg-log'
    modules = ['paste', 'simplejson', 'pyyaml']
    print 'log: %s' % egg_log
    print 'assuming setuptools is available.'
    for module in modules:
        print 'module: ' + module
        r = os.system("easy_install -maxzd %s %s >> %s" % (egg_target, module, egg_log))
        if r != 0:
            print
            print 'trouble!'
            print 'wanted to easy_install modules but failed.'
            # pause.
            print "press ENTER to continue the installation or CTRL-C to break."
            try: sys.stdin.readline()
            except KeyboardInterrupt:
                print "ok."
                sys.exit(1)
    print 'python eggs shelled in ' + egg_target


def setup():
    """calls setup.py"""
    print
    print "installing zohmg egg:"

    # install,
    r = os.system(sys.executable + ' setup.py install > /tmp/zohmg-install.log')
    if r != 0:
        # try once more immediately; usually works.
        r = os.system('python setup.py install > /tmp/zohmg-install.log')
        if r != 0:
            print 'trouble!'
            print 'could not install zohmg: python setup.py install'
            print 'log is at /tmp/zohmg-install.log'
            sys.exit(r)

    # let the user know what happened,
    os.system("egrep '(Installing|Copying) zohmg' /tmp/zohmg-install.log")
    # clean up.
    os.system("rm -rf build dist zohmg.egg-info")

def test():
    print 'testing zohmg script:'
    r = os.system('zohmg 2>&1 > /dev/null')
    if r != 0:
        # fail!
        print 'trouble!'
        print 'test run failed; it seems something is the matter with the installation :-|'
        sys.exit(r)
    print 'ok!'


# copies bundle (file) to destination, printing msg.
def copy_file(msg, file, destination):
    os.system("cp -v %s %s" % (file, destination))



if __name__ == "__main__":

    # check for rootness.
    if os.geteuid() != 0:
        print "you need to be root. please sudo."
        sys.exit(1)

    clean()
    copy_files()
    python_modules()
    setup()
    test()

    print
    print "ok, that should do it!"
    print "now try this:"
    print "$> zohmg help"
    print
