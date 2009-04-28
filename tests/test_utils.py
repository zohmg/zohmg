import unittest
from zohmg.utils import compare_triples

class TestUtils(unittest.TestCase):
    def test_tuplecompare(self):
        k = (10, 2, 'whatever')
        l = (10, 1, 'whatever')
        m = (0, 200, 'whatever')

        self.assertEqual(compare_triples(k, k), 0)
        self.assertEqual(compare_triples(k, l), 1)
        self.assertEqual(compare_triples(l, k), -1)
        self.assertEqual(compare_triples(k, m), 1)
        self.assertEqual(compare_triples(m, k), -1)


if __name__ == "__main__":
    unittest.main()
