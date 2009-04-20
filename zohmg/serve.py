
class Serve(object):
    def __init__(self, port=8086, host = 'localhost'):
        from zohmg.app import App
        from zohmg.config import Config
        from paste import httpserver
        import time

        c = Config()
        print "[%s] dataset: %s." % (time.asctime(), c.project_name())

        zapp = App(c.project_name())
        httpserver.serve(zapp.app, host=host, port=port)
