import os, shutil, sys

python_version = sys.version[:3] # works for now.

# FHS-compliant.
target     = '/usr/local/share/zohmg'
doc_target = '/usr/local/share/zohmg/doc'
lib_target = '/usr/local/lib/zohmg'
system_target  = '/usr/lib/python'+python_version+'/site-packages'


def clean():
	"""cleans things a bit."""
	print 'cleaning previous zohmg installation.'
	for dir in [target, doc_target, lib_target]:
		os.system("rm -rf %s" % dir)

def install():
    build_darling = False

    # check for rootness.
    if os.geteuid() != 0:
        print "you need to be root. please sudo."
        sys.exit(1)
    print "installing!"

    # create share and doc directories.
    for dir in [target,doc_target,lib_target]:
        if not os.path.isdir(dir):
            os.mkdir(dir)

    # darling.
    if build_darling:
        build_darling(target)
    else:
        copy_bundle("pre-built darling jar","lib/darling-*.jar",lib_target)

    # thrift & hbase.
    # TODO: don't bundle these eggs; easy_install them.

    # copies thrift egg.
    copy_bundle("bundled thrift egg","lib/thrift-*.egg",system_target)
    # copies hbase egg.
    copy_bundle("bundled hbase egg","lib/hbase-*.egg",system_target)
    # copies hbase thrift interface.
    copy_bundle("bundled hbase thrift interface","lib/Hbase.thrift",target)

    # docs.
    docs = ['README','TODO','QUICKSTART']
    for doc in docs:
        copy_bundle(doc,doc,doc_target)

    # examples.
    # TODO: fails if directory exists.
    shutil.copytree("examples",target+"/examples")

    # data server middleware.
    shutil.copytree("zohmg/middleware",lib_target+"/middleware")

    # libs.
    copy_bundle("dumbo mapper import script","src/import.py",lib_target)


def setup():
    print
    print "installing zohmg: python setup.py install"
	# install,
    r = os.system('python setup.py install > tmp/zohmg-install.log')
    if r != 0:
        print "errors?!"
        print "try again, it could work the second (or third) time."
        sys.exit(r)
	# let the user know what happened,
    os.system("egrep '(Installing|Copying) zohmg' tmp/zohmg-install.log")
    # clean up.
    os.system("rm -rf build dist zohmg.egg-info")

# not used atm; user would have to specify classpath == jobbigt.
def build_darling(target):
    print 'building java hook-ups'
    r = os.system('cd java/darling; ant')
    if r != 0:
        # fail!
        print 'problems building darling!'
        print 'hey, I need to know where to find jars for hbase, hadoop and hadoop streaming.'
        print 'please add them to $CLASSPATH and try again.'
        sys.exit(r)
    os.system("cp -v java/darling/build/darling-.jar " + target)

# copies bundle (file) to target, printing msg.
def copy_bundle(msg,file,target):
    print "copying",msg
    os.system("cp -v %s %s" % (file,target))
