from zohmg.config import Config
import simplejson as json

class Reducer(object):
    def __init__(self):
        #self.reduces = self.counters['reduces']
        self.config = Config()

    def __call__(self, key, values):
        #self.reduces += 1
        ts, ps, dims, unit = key
        value = sum(values)

        # rowkey: "unit-ymd".
        rk = '-'.join([unit, str(ts)])

        # construct column-family and qualifier strings.
        cflist = []
        qlist  = []
        for p in ps:
            cflist.append(p)
            qlist.append(dims[p])
        cf = '-'.join(cflist)
        q  = '-'.join(qlist)

        # remember, we'll pass the output of this reducer to HBaseOutputReader.
        yield rk, json.dumps({cf+":"+q : {'value':value}})

