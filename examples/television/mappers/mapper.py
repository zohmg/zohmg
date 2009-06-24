import time

def map(key, value):
    # split on space; make sure there are 7 parts.
    parts = value.split(' ')
    if len(parts) < 7: return

    # extract values.
    epoch = parts[0]
    clipid, producerid, length = parts[1:4]
    country, player, love      = parts[4:7]

    # format timestamp as yyyymmdd.
    ymd = "%d%02d%02d" % time.localtime(float(epoch))[0:3]

    # dimension attributes are strings.
    dimensions = {}
    dimensions['clip']     = str(clipid)
    dimensions['producer'] = str(producerid)
    dimensions['country']  = country
    dimensions['player']   = player

    # measurements are integers.
    measurements = {}
    measurements['plays']   = 1
    measurements['seconds'] = int(length)
    measurements['loves']   = int(love)

    yield ymd, dimensions, measurements
