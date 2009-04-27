import time

class client(object):
    """
    Application that serves static files from the client/ directory in the
    project directory.
    """
    def __call__(self,environ,start_response):
        from paste.urlparser import make_static
        print "[%s] Client, serving static file." % time.asctime()
        project_dir = environ.get("zohmg_project_dir","")
        client = make_static({},project_dir+"/clients")
        return client(environ,start_response)
