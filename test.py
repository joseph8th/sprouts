#!/usr/bin/env python2

from sprouts.models import *
from sprouts.game import *
from sprouts.views import *

test_pos_l = ['1,2;3;4;5/1,2', '1,2;3/1,2',]

for test_pos in test_pos_l:
    print "Testing: ", test_pos
    p = Position(test_pos)
    g = SproutsGame(p)
    t = GameTree(g)

    Report(t)
