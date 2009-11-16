import unittest
import helper
from useragent import UserAgent

class TestUserAgent(unittest.TestCase):
    def test_classify(self):
        user_agent_string = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-GB; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'
        ua = UserAgent(user_agent_string)
        self.assertEqual(ua.classify(), "firefox")
        self.assertTrue(ua.is_browser())
        self.assertFalse(ua.is_robot())

if __name__ == '__main__':
    unittest.main()
