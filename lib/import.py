#!/usr/bin/env python
# the script we tell dumbo to run.

import dumbo
from zohmg.mapper import Mapper
from zohmg.reducer import Reducer
from zohmg.combiner import Combiner
from usermapper import map
dumbo.run(Mapper(map), Reducer(), Combiner())
