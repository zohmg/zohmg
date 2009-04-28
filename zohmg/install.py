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

# hey, what's the difference between install and setup?
def install():
    build_darling = False

    # check for rootness.
    if os.geteuid() != 0:
        print "you need to be root. please sudo."
        sys.exit(1)
    print "installing!"

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

    # thrift & hbase, etc.
	print "installing libraries with no installation mechanism of their own - the eggdance."
	os.system("sh eggs/eggdance.sh")

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

def test():
	sys.stdout.write('testing zohmg script..')
	r = os.system('zohmg &> /dev/null')
	if r != 0:
		# fail!
		print 'fail.'
		print 'test run failed; it seems something is the matter with the installation :-|'
		sys.exit(r)
	else:
		print 'ok!'



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
