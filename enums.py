# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 10:08:32 2017

@author: Pablo
"""
from enum import Enum

class State(Enum):
    Unasked = 0
    Wrong = 1
    Right = 2
    
class strategies(Enum):
    top_down = 0
    divide_and_query = 1