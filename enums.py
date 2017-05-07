# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 10:08:32 2017

@author: Pablo
"""
from enum import Enum

class State(Enum):
    UNASKED = 0
    WRONG = 1
    RIGHT = 2


class Strategy(Enum):
    TOP_DOWN = 0
    DIVIDE_AND_QUERY = 1
    TOP_DOWN_HEAVIEST_FIRST = 2