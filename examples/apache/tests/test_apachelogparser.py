import unittest
import helper
from apachelogparser import ApacheLogParser

class TestApacheLogParser(unittest.TestCase):
    def test_parse(self):
        log = '85.229.87.106 - - [15/Nov/2009:18:01:25 +0000] '\
              '"GET / HTTP/1.1" 200 883 "-" "firefox"'
        parsed = ApacheLogParser().parse(log)
        self.assertEqual(parsed['host'], '85.229.87.106')
        self.assertEqual(parsed['timestamp'], '2009-11-15 18:01:25')
        self.assertEqual(parsed['epoch'], 1258308085)
        self.assertEqual(parsed['method'], 'GET')
        self.assertEqual(parsed['path'], '/')
        self.assertEqual(parsed['status'], '200')
        self.assertEqual(parsed['size'], '883')
        self.assertEqual(parsed['referrer'], '-')
        self.assertEqual(parsed['agent'], 'firefox')

if __name__ == '__main__':
    unittest.main()
