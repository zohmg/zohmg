import unittest
import helper
import apache

class TestMap(unittest.TestCase):
    def test_map(self):
        logline = '85.229.87.106 - - [15/Nov/2009:18:01:25 +0000] '\
                  '"GET / HTTP/1.1" 200 883 "-" "firefox"'

        ts, dimensions, measurements = apache.map(0, logline).next()

        # ts => 20091115
        # ds => {'status': '200', 'referrer': '-', 'agent': 'firefox',
        #        'host': '85.229.87.106', 'path': '/', 'method': 'GET'}
        # ms => {'requests': 1, 'bytes': 883}

        self.assertEqual(ts, "20091115")
        for d in ['host', 'method', 'path', 'status', 'referrer', 'agent']:
            self.assertTrue(d in dimensions)
        self.assertEqual(measurements['bytes'], 883)
        self.assertEqual(measurements['requests'], 1)

if __name__ == '__main__':
    unittest.main()
