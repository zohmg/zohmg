import unittest
from zohmg.config import Config

class TestConfig(unittest.TestCase):
    def test_sanity_check(self):
        # a few broken configurations,
        for x in ['a','b', 'c']:
            print x
            dataset = 'tests/fixtures/dataset-broken-%s.yaml' % x
            c = Config(dataset)
            self.assertEqual(c.sanity_check(), False)
        # and a good one.
        dataset = 'tests/fixtures/dataset-ok.yaml'
        c = Config(dataset)
        self.assertEqual(c.sanity_check(), True)

if __name__ == "__main__":
    unittest.main()
