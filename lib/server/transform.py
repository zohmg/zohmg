#!/usr/bin/env python

import time


class transform(object):
    def __init__(self):
        # TODO: urlparser middlewaring/plugins for transformations.
        print "[%s] Initialized transform app." % time.asctime()
        self.str = "transform"

    def __call__(self,environ,start_response):
        # TODO: urlparser to correct plugin.
        print "[%s] Call to transform app." % time.asctime()
        start_response("200 OK",[("Content-type","text/html")])
        return self.str
