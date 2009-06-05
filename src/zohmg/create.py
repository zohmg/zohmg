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

import os, sys, shutil
from zohmg.utils import fail

class Create(object):
    def __init__(self, path):
        self.basename = os.path.basename(path)
        self.abspath  = os.path.abspath(path)

        print ("creating project directory %s " % self.abspath)
        try:
            shutil.copytree('/usr/local/share/zohmg/skel-project', self.abspath)
        except OSError, ose:
            # something went wrong. act accordingly.
            msg = "error: could not create project directory. %s" % ose.strerror
            fail(msg, ose.errno)

        # set name of dataset in dataset.yaml
        dataset_path = self.abspath + '/config/dataset.yaml'
        os.system("sed 's/DATASETNAME/%s/' %s  > /tmp/dataset.yaml" % (self.basename, dataset_path))
        os.system("mv /tmp/dataset.yaml " + dataset_path)

        print "ok."
