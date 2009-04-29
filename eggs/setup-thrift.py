from setuptools import setup

# these are the thrift python codes
# downloaded from http://svn.apache.org/repos/asf/incubator/thrift/trunk/lib/py/ at some time in the afternoon.
# it is entirely unclear what version this really is - a comment on the current state of open source software engineering at facebook.

# TODO: check klaas' packaging here: http://pypi.python.org/pypi/thrift/1.0
# and/or svn co http://svn.apache.org/repos/asf/incubator/thrift/trunk/lib/py 

setup(name='thrift', version='0.0.x-random', packages=['thrift', 'thrift/protocol', 'thrift/reflection', 'thrift/server', 'thrift/transport'],)
