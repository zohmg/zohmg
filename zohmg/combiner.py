class Combiner(object):
    def __init__(self):
        pass

    def __call__(self, key, values):
        yield key, sum(values)
