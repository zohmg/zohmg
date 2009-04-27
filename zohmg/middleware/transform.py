#!/usr/bin/env python

import time


class transform(object):
    def __call__(self,environ,start_response):
        project_dir = environ["zohmg_project_dir"]
        print "[%s] Transform, erving from %s." % (time.asctime(),project_dir)
        start_response("200 OK",[("Content-type","text/html")])
        return self.str
