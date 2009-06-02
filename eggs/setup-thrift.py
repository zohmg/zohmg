#Licensed to the Apache Software Foundation (ASF) under one
#or more contributor license agreements.  See the NOTICE file
#distributed with this work for additional information
#regarding copyright ownership.  The ASF licenses this file
#to you under the Apache License, Version 2.0 (the
#"License"); you may not use this file except in compliance
#with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing,
#software distributed under the License is distributed on an
#"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#KIND, either express or implied.  See the License for the
#specific language governing permissions and limitations
#under the License.

from setuptools import setup

# these are the thrift python codes
# downloaded from http://svn.apache.org/repos/asf/incubator/thrift/trunk/lib/py/ at some time in the afternoon.
# it is entirely unclear what version this really is - a comment on the current state of open source software engineering at facebook.

# TODO: check klaas' packaging here: http://pypi.python.org/pypi/thrift/1.0
# and/or svn co http://svn.apache.org/repos/asf/incubator/thrift/trunk/lib/py 

setup(name='thrift', version='0.0.x-random', packages=['thrift', 'thrift/protocol', 'thrift/reflection', 'thrift/server', 'thrift/transport'],)
