from zohmg.utils import fail


class Environ(object):
    def __init__(self):
        self.environ = {}
        self.read_environ()

    def get(self,key):
        return self.environ[key]

    def read_environ(self):
        sys.path.append("") # add cwd so we can import from it.
        try:
            env = __import__("config/environment")
        except ImportError, ioe:
            msg = "E: Could not import config/environment.py. %s" % ioe.strerror
            fail(msg,ioe.errno)

        for key in dir(env):
            self.environ[key] = env.__dict__[key]

