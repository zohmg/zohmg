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

import string, sys, time
from random import Random

def random_string(size):
    # subopt for larger sizes.
    if size > len(string.letters):
        return random_string(size/2)+random_string(size/2)
    return ''.join(Random().sample(string.letters, size))


def timing(func):
    def wrapper(*arg):
        t0 = time.time()
        r = func(*arg)
        elapsed = time.time() - t0
        return (elapsed*1000.00)
    return wrapper


def timing_p(func):
    def wrapper(*arg):
        t0 = time.time()
        r = func(*arg)
        elapsed = (time.time() - t0) * 1000.00
        print "=> %.2f ms" % elapsed
        return elapsed
    return wrapper

#
# General helpers
#
def compare_triples(p, q):
    """
    p and q are triples, like so: (4, 2, ..)
    sort by first the element, then by the second. don't care about the third element.
    return 1, 0, or -1 if p is larger than, equal to, or less than q, respectively.
    """
    a, b, dontcare = p
    x, y, dontcare = q
    if a > x: return  1
    if a < x: return -1
    if b > y: return  1
    if b < y: return -1
    return 0


def fail(msg,errno=1):
    print >>sys.stderr, msg
    exit(errno)


# strip whitespaces.
def strip(str):
    return str.strip()
