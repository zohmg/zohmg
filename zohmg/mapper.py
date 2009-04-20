from zohmg.config import Config

class Mapper(object):
    def __init__(self, usermapper):
        self.usermapper = usermapper
        self.projections = Config().projections()

    # wrapper around the user's mapper.
    def __call__(self, key, value):
        # from the usermapper: a timestamp, a point in n-space, units and their values.
        for (ts, point, units) in self.usermapper(key, value):
            for pjs in self.projections.values():
                # we perform dimensionality reduction,
                reduced = {}
                for d in pjs:
                    reduced[d] = point[d]
                # yielding for each requested projection.
                for u in units:
                    value = units[u]
                    yield (ts, reduced, u), value
