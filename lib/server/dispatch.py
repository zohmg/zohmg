#!/usr/bin/env python


class Dispatch(object):
    def __init__(self):
        from paste.urlparser import make_url_parser
        self.app = make_url_parser({},".","")

    def __call__(self,environ,start_response):
        self.app(environ,start_response)


if __name__ == "__main__":
    from paste import httpserver

    app = Dispatch()
    httpserver.serve(app,host="localhost",port="8086")
