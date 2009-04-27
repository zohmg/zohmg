#!/usr/bin/env python

import sys, time
import simplejson as json

from paste.request import parse_formvars

from zohmg.scanner import HBaseScanner
from zohmg.config import Config


class data(object):
    def __init__(self):
        from zohmg.config import Config
        self.dataset = Config().dataset()
        print "[%s] Initialized data server. Dataset: %s." % (time.asctime(), self.dataset)

    def __call__(self,environ,start_response):
        print "[%s] Call to data app. Dataset: %s." % (time.asctime(), self.dataset)
        start_response("200 OK",[("Content-type", "text/html")])
        return "data"
