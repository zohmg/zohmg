# user's mapper.
def map(key, value):
    from lfm.data.parse import web

    try: log = web.Log(value)
    except ValueError: return
    ua = web.UserAgent()

    ts = log.timestamp.ymd()
    dimensions = {'country'   : log.country(),
                  'domain'    : log.domain,
                  'useragent' : ua.classify(log.agent),
                  'usertype'  : ("user", "anon")[log.userid == None]
                  }
    values = {'pageviews' : 1}
    
    yield ts, dimensions, values
