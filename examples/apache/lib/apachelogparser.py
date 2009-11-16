import calendar, time, re

class ApacheLogParser:
    def __init__(self):
        # regex for the 'combined' log format.
        self.regex = re.compile(r'''
                                ^([0-9\.]+)\          # IP address
                                [^ ]+\                # ignore
                                [^ ]+\                # ignore
                                \[([^ ]+)[^\]]+\]\    # timestamp
                                "([A-Z]+)\            # method
                                ([^ ]+)[^"]+"\        # path
                                ([0-9\-]+)\           # status
                                ([0-9\-]+)\           # size
                                "([^"]+)"\            # referrer
                                "([^"]+)"             # agent
                                ''', re.VERBOSE)
        # example of log line:
        # 85.229.87.106 - - [15/Nov/2009:18:01:25 +0000]
        # "GET / HTTP/1.1" 200 883 "-"
        # "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-GB; rv:1.9.1.5)
        # Gecko/20091102 Firefox/3.5.5"

    def parse(self, line):
        """parses log line, returns dict."""
        parsed = {}
        try:
            mo = self.regex.search(line)
            parsed['host'] = mo.group(1)
            parsed['timestamp'], parsed['epoch'] = self.timestamps(mo.group(2))
            parsed['method']   = mo.group(3)
            parsed['path']     = mo.group(4)
            parsed['status']   = mo.group(5)
            parsed['size']     = mo.group(6)
            parsed['referrer'] = mo.group(7)
            parsed['agent']    = mo.group(8)
        except AttributeError: raise ValueError()
        return parsed

    def timestamps(self, timestamp):
        """parses timestamp of format 15/Nov/2009:18:01:25
        assumes timestamp is in UTC
        returns tuple of (formatted_timestamp, epoch)"""
        time_struct = time.strptime(timestamp, "%d/%b/%Y:%H:%M:%S")
        formatted = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
        epoch = calendar.timegm(time_struct)
        return formatted, epoch
