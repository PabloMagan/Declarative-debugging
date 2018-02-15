# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:52:12 2017

@author: Pablo Magan Hernandez
"""
import debuggingtree as dt
from enums import State, Strategy
import copy

class DeclarativeDebugging(object):
    def __init__(self,tree):
        self.strategy = Strategy.TOP_DOWN
        self.undo_list = [tree]
        self.tree = tree
        
    def depuracion_declarativa(self):
        buggy = self.tree.getBuggyNode()
        while buggy == None:
            self.ask()
            buggy = dt.tree.getBuggyNode()
        buggy.paint_state(0)
        return buggy
    
    def ask(self):
        self.undo_list.append(copy.deepcopy(self.tree))
        if self.strategy == Strategy.TOP_DOWN:
            node = self.tree.top_down()
        elif self.strategy == Strategy.DIVIDE_AND_QUERY:
            node = self.tree.divide_and_query()
        elif self.strategy == Strategy.TOP_DOWN_HEAVIEST_FIRST:
            node = self.tree.top_down_heaviest_first()
        print(node.fun, node.arg,"->", node.ret,node.out)
        print ('write td, dq, or tdhf to change the strategy')
        answer = input("Is that right?: ")
        
        if answer == "yes":
            tree = self.tree
            dt.tree.colour_tree(node, State.RIGHT)
            self.tree = tree
            self.tree.update_weight()
        elif answer == "no":
            tree = self.tree
            dt.tree.colour_tree(node, State.WRONG)
            self.tree = tree
            self.tree.update_weight()
        elif answer == "undo":
            self.tree = self.undo_list[0]
            self.tree.paint_state(1)
            self.undo_list = self.undo_list[:-1]
        elif answer == "td":
            self.strategy = Strategy.TOP_DOWN
        elif answer == "dq":
            self.strategy = Strategy.DIVIDE_AND_QUERY
        elif answer == "tdhf":
            self.strategy = Strategy.TOP_DOWN_HEAVIEST_FIRST
            




depurar = DeclarativeDebugging(dt.tree)