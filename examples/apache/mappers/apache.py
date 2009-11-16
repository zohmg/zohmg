# analyze log files from the apache web server.
# log lines are in the 'combined' format.

from apachelogparser import ApacheLogParser
import time

def ymd(epoch):
    """formats a unix timestamp as string of format yyyymmdd
    ymd(1258308085) => '20091115'"""
    time_tuple = time.gmtime(epoch)
    return time.strftime("%Y%m%d", time_tuple)

def map(key, logline):
    parsed = ApacheLogParser().parse(logline)

    # timestamp of format yyyymmdd.
    timestamp = ymd(parsed['epoch'])

    # dimension attributes are strings.
    dimensions = {}
    dimensions['host']     = parsed['host']
    dimensions['method']   = parsed['method']
    dimensions['path']     = parsed['path']
    dimensions['status']   = parsed['status']
    dimensions['referrer'] = parsed['referrer']
    dimensions['agent']    = parsed['agent']

    # measurements are integers.
    measurements = {}
    measurements['bytes'] = int(parsed['size'])
    measurements['requests'] = 1

    yield timestamp, dimensions, measurements
