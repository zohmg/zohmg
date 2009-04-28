import time

class client(object):
    """
    Application that serves static files from the client/ directory in the
    project directory.
    """
    def __call__(self,environ,start_response):
        from paste.urlparser import make_static
        project_dir = environ["zohmg_project_dir"]
        file = environ["PATH_INFO"]
        client = make_static({},project_dir+"/clients")
        print "[%s] Client, serving static file %s%s." % (time.asctime(),project_dir,file)
        return client(environ,start_response)
