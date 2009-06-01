import unittest
from zohmg.config import Config

class TestConfig(unittest.TestCase):
    def test_sanity_check(self):
        # a few broken configurations,
        for x in ['a','b', 'c']:
            dataset = 'tests/fixtures/dataset-broken-%s.yaml' % x
            self.assertRaises(SystemExit, Config, dataset)
        # and a good one.
        dataset = 'tests/fixtures/dataset-ok.yaml'
        c = Config(dataset)
        self.assertEqual(c.sanity_check(), True)

if __name__ == "__main__":
    unittest.main()
