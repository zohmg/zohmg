class Environment(object):
    def __init__(self):
        self.environ = {}
        self.read_environ()

    def get(self,key):
        return self.environ[key]

    def read_environ(self):
        sys.path.append("") # add cwd
        try:
            env = __import__("config/environment")
        except ImportError:
            print >> sys.stderr,"E: Could not import config/environment.py, does it exist?"
            exit(1)

        for key in dir(env):
            self.environ[key] = env.__dict__[key]

