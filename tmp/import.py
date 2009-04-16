#!/usr/bin/env python
# the script we tell dumbo to run.

import dumbo
from zohmg import Mapper, Reducer
from usermapper import map
dumbo.run(Mapper(map), Reducer)
