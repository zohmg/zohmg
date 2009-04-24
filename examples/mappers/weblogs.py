# user's mapper.
#
# this piece of code assumes that the Apache common log format,
# see http://httpd.apache.org/docs/2.0/logs.html for more info.


def map(key,value):
    # parse log string, extract year, month and day
    import re
    mo = re.search(r"\[(\d{2})/(\w{3})/(\d{4})",value) # [20/Apr/2009
    year  = mo.group(3)
    month = mo.group(2)
    day   = mo.group(1)

    time  = year + month + day
    dimensions = {'user'   : value.split(" ")[2],
                  'status' : value.split(" ")[8]
                 }
    values = {'pageviews' : 1}

    yield time,dimensions,values
