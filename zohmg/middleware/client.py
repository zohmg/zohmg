class client(object):
    def __init__(self,project_dir):
        from paste.urlparser import make_static
        # TODO: THIS IS HARD WIRED FOR NOW
        project_dir = "/home/per/zapps/webmetrics"
        self.client = make_static({},project_dir+"/clients","")

    def __call__(self,environ,start_response):
        return self.client
