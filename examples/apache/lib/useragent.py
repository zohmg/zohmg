import re

class UserAgent:
    browsers = [("Mozilla.*MSIE ([^;]+);.*"           , 'ie'),
                ("Opera/([^ ]+).*|.*Opera ([^ ;]+).*" , 'opera'),
                (".*Firefox/([^ ,;/()']+).*"          , 'firefox'),
                (".* Chrome/([^ ,;/()']+).*"          , 'chrome'),
                (".*Safari/([^ ,)]+).*"               , 'safari'),
                (".*AppleWebKit/([^ )]+).*"           , 'webkit'), # generic webkit
                (".*rv:([^ ;)]+)\\) Gecko/\\d+.*"     , 'gecko')]  # generic gecko
    crawlers = [("Mozilla.*Googlebot/.*", 'google'),
                ("Mozilla.*Ask Jeeves/Teoma.*", 'askjeeves'),
                ("Mozilla.*Yahoo! Slurp.*", 'yahooslurp'),
                ("facebookplatform/.*", 'facebook'),
                ("Baiduspider.*", 'baidu'),
                ("msnbot.*", 'msn')]

    def __init__(self, user_agent_string):
        self.user_agent_string = user_agent_string
        # compile regexes.
        self.browser_patterns = self.compile_patterns(self.browsers)
        self.crawler_patterns = self.compile_patterns(self.crawlers)

    def classify(self):
        for pattern, agent in self.browser_patterns + self.crawler_patterns:
            if pattern.search(self.user_agent_string): return agent
        return 'other'

    def is_browser(self):
        for pattern, agent in self.browser_patterns:
            if pattern.search(self.user_agent_string): return True
        return False

    def is_robot(self):
        for pattern, agent in self.crawler_patterns:
            if pattern.search(self.user_agent_string): return True
        return False


    def compile_patterns(self, patterns):
        compiled = []
        for p, i in patterns:
            compiled.append((re.compile(p), i))
        return compiled

