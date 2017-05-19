# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:52:12 2017

@author: adrian
"""
import debuggingtree as dt
from enums import State, Strategy

class DepuracionDeclarativa(object):
    def __init__(self,arbol):
        self.strategy = Strategy.DIVIDE_AND_QUERY
        self.undo_list = []
        self.tree = arbol
        
    def depuracion_declarativa(self):
        buggy = self.tree.getBuggyNode()
        while buggy == None:
            self.ask()
            arbol = self.tree
            #TODO: Esto en algún momento habrá que arreglarlo, porque depura
            # la variable global arbol del otro fichero, la variable local no vale para nada
            buggy = dt.arbol.getBuggyNode()
        buggy.pintarest(0)
        return buggy
    
    def ask(self):
        self.undo_list.append(self.tree)
        if self.strategy == Strategy.TOP_DOWN:
            nodo = self.tree.top_down()
        elif self.strategy == Strategy.DIVIDE_AND_QUERY:
            nodo = self.tree.divide_and_query()
        elif self.strategy == Strategy.TOP_DOWN_HEAVIEST_FIRST:
            nodo = self.tree.top_down_heaviest_first()
        
        print(nodo.f, nodo.arg,"->", nodo.res)
        print ('write td, dq, or tdhf to change the strategy')
        respuesta = input("Is that right?: ")
        
        if respuesta == "yes":
            arbol = self.tree
            dt.arbol.colour_tree(nodo, State.RIGHT)
            self.tree = arbol
            self.tree.update_weight()
        elif respuesta == "no":
            arbol = self.tree
            dt.arbol.colour_tree(nodo, State.WRONG)
            self.tree = arbol
            self.tree.update_weight()
        elif respuesta == "undo":
            self.tree = self.undo_list[-2]
            self.undo_list = self.undo_list[:-2]
        elif respuesta == "td":
            self.strategy = Strategy.TOP_DOWN
        elif respuesta == "dq":
            self.strategy = Strategy.DIVIDE_AND_QUERY
        elif respuesta == "tdhf":
            self.strategy = Strategy.TOP_DOWN_HEAVIEST_FIRST
            




depurar = DepuracionDeclarativa(dt.arbol)