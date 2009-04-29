import os, shutil, sys

python_version = sys.version[:3] # works for now.

# FHS-compliant.
target     = '/usr/local/share/zohmg'
doc_target = '/usr/local/share/zohmg/doc'
lib_target = '/usr/local/lib/zohmg'
system_target  = '/usr/lib/python'+python_version+'/site-packages' # might bork on 2.6


def clean():
    """cleans things a bit."""
    print
    print 'cleaning previous zohmg installation.'
    os.system("rm %s/zohmg-*.egg 2> /dev/null" % system_target)
    for dir in [target, doc_target, lib_target]:
        os.system("rm -rf %s" % dir)

def install():
    print
    print "installing python modules &c."

    # apt-get python modules.
    install_pythonmodules()

    # thrift & hbase, etc.
    #requires setuptools.
    print "installing libraries with no installation mechanism of their own - the eggdance."
    os.system("sh eggs/eggdance.sh")


def copy_files():
    print
    print "populating zohmg directories"

    build_darling = False

    # creating directories.
    for dir in [target, doc_target, lib_target]:
        if not os.path.isdir(dir):
            os.mkdir(dir)

    # copy docs.
    docs = ['README','TODO','QUICKSTART']
    for doc in docs:
        copy_bundle(doc,doc,doc_target)

    # darling.
    if build_darling:
        build_darling(target)
    else:
        copy_bundle("pre-built darling jar","lib/darling-*.jar",lib_target)

    # HBase.thrift
    copy_bundle("bundled hbase thrift interface","lib/Hbase.thrift",target)

    # copy examples.
    shutil.copytree("examples",target+"/examples")

    # data server middleware.
    shutil.copytree("zohmg/middleware",lib_target+"/middleware")

    # libs.
    copy_bundle("dumbo mapper import script","src/import.py",lib_target)


def setup():
    print
    print "installing zohmg"

    # install,
    r = os.system('python setup.py install > zohmg-install.log')
    if r != 0:
        print "errors?!"
        print "try again, it could work the second (or third) time."
        sys.exit(r)
    # let the user know what happened,
    os.system("egrep '(Installing|Copying) zohmg' zohmg-install.log")
    # clean up.
    os.system("rm -rf build dist zohmg.egg-info")

def test():
    sys.stdout.write('testing zohmg script..')
    r = os.system('zohmg 2>&1 > /dev/null')
    if r != 0:
        # fail!
        print 'fail.'
        print 'test run failed; it seems something is the matter with the installation :-|'
        sys.exit(r)
    else:
        print 'ok!'



# not used atm; user would have to specify classpath == jobbigt.
def build_darling(target):
    print
    print 'building java hook-ups'

    r = os.system('cd java/darling; ant')
    if r != 0:
        # fail!
        print 'problems building darling!'
        print 'hey, I need to know where to find jars for hbase, hadoop and hadoop streaming.'
        print 'please add them to $CLASSPATH and try again.'
        sys.exit(r)
    os.system("cp -v java/darling/build/darling-.jar " + target)

def install_pythonmodules():
    packages = ['python-setuptools', 'python-paste', 'python-simplejson', 'python-yaml']
    print 'apt-get installing pythonmodules; assuming your system is debian-based. '
    print ', '.join(packages) + '.'
    r = os.system('sudo apt-get install ' + ' '.join(packages))
    if r != 0:
        print 'problems apt-getting packages!'
        print 'please make sure you install the following packages or their equivalents:'
        for p in packages: print "* " + p
        print

# copies bundle (file) to target, printing msg.
def copy_bundle(msg,file,target):
    os.system("cp -v %s %s" % (file,target))
