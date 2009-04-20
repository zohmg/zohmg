#!/usr/bin/env python

import time


class Dispatch(object):
    def __init__(self):
        from paste.urlparser import make_url_parser
        self.dispatch = make_url_parser({},".","")

    def __call__(self,environ,start_response):
        return self.dispatch(environ,start_response)


if __name__ == "__main__":
    from paste import httpserver

    app = Dispatch()
    print "[%s] Initialized data server dispatcher." % time.asctime()
    httpserver.serve(app,host="localhost",port="8086")
