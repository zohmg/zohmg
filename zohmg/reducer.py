from zohmg.config import Config
import simplejson as json

class Reducer(object):
    def __init__(self):
        self.config = Config()

    def __call__(self, key, values):
        ts, ps, dims, unit = key
        value = sum(values)

        # rowkey: "unit-ymd".
        rk = '-'.join([unit, str(ts)])

        # construct column-family and qualifier strings.
        # it's important that we get the ordering right.
        cflist = []
        qlist  = []
        for p in ps:
            cflist.append(p)
            qlist.append(dims[p])
        cf = '-'.join(cflist)
        q  = '-'.join(qlist)

        # remember, we'll pass the output of this reducer to HBaseOutputReader.
        yield rk, json.dumps({cf+":"+q : {'value':value}})

