from zohmg.config import Config
import simplejson as json

class Reducer(object):
    def __init__(self):
        #self.reduces = self.counters['reduces']
        self.config = Config()

    def __call__(self, key, values):
        #self.reduces += 1
        ts, dims, unit = key
        value = sum(values)

        # rowkey: "unit-ymd".
        rk = '-'.join([unit, str(ts)])
        cf = '-'.join(dims.keys())
        q  = '-'.join(dims.values())

        # remember, we'll pass the output of this reducer to HBaseOutputReader.
        yield rk, json.dumps({cf+":"+q : {'value':value}})

