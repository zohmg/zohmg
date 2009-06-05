def map(key, value):
    # you will want to analyze value, obviously.

    # timestamp is of format yyyymmdd.
    timestamp = "20090605"

    # dimension attributes are strings.
    dimensions = {'fruit': 'apple',
                  'producer': 'del monte',
                  'color': 'red',
                  'size': 'largeish'}

    # measurements are integers.
    measurements = {}
    measurements['seeds'] = 3
    measurements['weight'] = 85 # grams

    yield timestamp, dimensions, measurements
