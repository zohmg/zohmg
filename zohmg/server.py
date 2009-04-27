#!/usr/bin/env python

import time


class Dispatch(object):
    def __init__(self,project_dir):
        from paste.urlparser import make_url_parser
        self.dispatch = make_url_parser({"project_dir":project_dir},"/usr/local/lib/zohmg/middleware","")
        print "[%s] Initialized data server dispatcher. Serving from %s." % (time.asctime(),project_dir)

    def __call__(self,environ,start_response):
        return self.dispatch(environ,start_response)


def start(project_dir,host="localhost",port="8086"):
    from paste import httpserver
    app = Dispatch(project_dir)
    httpserver.serve(app,host=host,port=port)
