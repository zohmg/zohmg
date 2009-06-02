from zohmg.config import Config

# exploding mapper!
class Mapper(object):
    def __init__(self, usermapper):
        self.usermapper = usermapper
        self.projections = Config().projections()

    # helper for generating all permutations of a dictionary.
    def dict_permutations(self, dict_):
        dict = dict_.copy()
        # base case.
        if len(dict) == 1:
            # {'agent': 'firefox'} => [{'agent': 'firefox'}, {'agent': 'all'}]
            return [dict, {dict.keys()[0] : 'all'}]

        x  = dict.popitem()
        xs = self.dict_permutations(dict)

        permuts = []
        for a in [x, (x[0], 'all')]:
            for b in xs: # b => {'agent': "firefox", 'country': "US"}
                b[a[0]] = a[1] # add a to b.
                permuts.append(b.copy())
        return permuts

    # wrapper around the user's mapper.
    def __call__(self, key, value):
        # from the usermapper: a timestamp, a point in n-space, units and their values.
        for (ts, point, units) in self.usermapper(key, value):
            for p in self.projections:
                # dimensionality reduction,
                reduced = {}
                for d in p:
                    reduced[d] = point[d]
                # yield for each requested projection.
                # include the projections list to get the order right.
                for u in units:
                    value = units[u]
                    for permut in self.dict_permutations(reduced):
                        # we yield len(projections) * len(units) * 2^len(reduced) times.
                        yield (ts, p, permut, u), value
