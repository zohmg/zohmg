#!/usr/bin/env python

import time


class data(object):
    def __init__(self):
        print "[%s] Initialized data app." % time.asctime()
        self.str = "data"

    def __call__(self,environ,start_response):
        print "[%s] Call to data app." % time.asctime()
        start_response("200 OK",[("Content-type", "text/html")])
        return self.str
