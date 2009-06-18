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

# user's mapper.
#
# this piece of code assumes that the Apache common log format,
# see http://httpd.apache.org/docs/2.0/logs.html for more info.


def map(key,value):
    # parse log string, extract year, month and day
    import re
    mo = re.search(r"\[(\d{2})/(\w{3})/(\d{4})",value) # [20/Apr/2009
    year  = mo.group(3)
    month = mo.group(2)
    day   = mo.group(1)

    time  = year + month + day
    dimensions = {'user'   : value.split(" ")[2],
                  'status' : value.split(" ")[8]
                 }
    values = {'pageviews' : 1}

    yield time,dimensions,values
