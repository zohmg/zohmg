def map(key, value):
    from lfm.data.parse import web
    log = web.Log(value)
    
    ts      = log.timestamp.unixtime()
    dimensions = {'country' : log.country(),
                  'domain'  : log.domain,
                  'useragent' : log.agent,
                  'usertype'  : ("user", "anon")[log.userid == None]
                  }
    values = {'pageviews':1}
    
    yield ts, dimensions, values
