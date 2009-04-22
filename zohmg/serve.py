class Serve(object):
    def __init__(self, port=8086, host='localhost'):
        from zohmg.app import App
        from zohmg.config import Config
        from paste import httpserver
        import time
        
        dataset = Config().dataset()
        zapp = App(dataset)
        print "[%s] enabling dataset %s." % (time.asctime(), dataset)
        httpserver.serve(zapp.app, host=host, port=port)
