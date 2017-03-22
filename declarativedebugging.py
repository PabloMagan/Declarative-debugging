# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:52:12 2017

@author: adrian
"""
import debuggingtree
from enums import State, Strategy

class DepuracionDeclarativa(object):
    def __init__(self,arbol):
        self.strategy = Strategy.TOP_DOWN
        self.undo_list = []
        self.tree = arbol
        
    def depuracion_declarativa(self):
        buggy = self.tree.getBuggyNode([])
        while buggy == None:
            self.ask()
            buggy = self.tree.getBuggyNode([])
        print(buggy)
        return buggy
    
    def ask(self):
        self.undo_list.append(self.tree)
        if self.strategy == Strategy.TOP_DOWN:
            nodo = self.tree.top_down()
        elif self.strategy == Strategy.DIVIDE_AND_QUERY:
            nodo = self.tree.divide_and_query()
        
        print(nodo.f, nodo.arg,"->", nodo.res)
        respuesta = input("Is that right?: ")
        
        if respuesta == "yes":
            #TODO: Pensar si recalcular pesos dentro de colour.
            self.colour_tree(nodo, State.RIGHT)
            self.tree.update_weight()
        elif respuesta == "no":
            self.colour_tree(nodo, State.WRONG)
            self.tree.update_weight()
        elif respuesta == "undo":
            self.tree = self.undo_list[-2]
            self.undo_list = self.undo_list[:-2]




depurar = DepuracionDeclarativa(debuggingtree.arbol)