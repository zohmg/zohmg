#!/usr/bin/env python

import os, sys, yaml
from zohmg import Config, Mapper, Reducer

if __name__ == "__main__":
    import dumbo
    from usermapper import map as usermap
    dumbo.run(Mapper(usermap), Reducer)
    # will want to use a combiner, too.
    # tried dumbo.sumreducer() but it ran into memory errors, which was weird.

