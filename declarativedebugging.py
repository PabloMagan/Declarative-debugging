# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:52:12 2017

@author: adrian
"""
from enum import Enum
import debuggingtree

class DepuracionDeclarativa(object):
    def __init__(self):
        self.strategy = strategies.top_down
        self.undo_list = []
        self.tree = None
        
    def depuracion_declarativa(self):
        while self.tree.getBuggyNode([]) != None:
            self.ask()
    
    def ask(self):
        self.undo_list.append(self.tree)
        if self.strategy == strategies.top_down:
            nodo = self.tree.top_down()
        elif self.strategy == strategies.divide_and_query:
            nodo = self.tree.divide_and_query()
        
        print(nodo.f, nodo.arg,"->", nodo.res)
        respuesta = input("Is that right?: ")
        
        if respuesta == "yes":
            nodo.modestados(2)
            self.tree.delete_tree(nodo)
            #quitar ese nodo
        elif respuesta == "no":
            self.tree = nodo
        elif respuesta == "undo":
            self.tree = self.undo_list[-2]
            self.undo_list = self.undo_list[:-2]

class strategies(Enum):
    top_down = 0
    divide_and_query = 1


depurar = DepuracionDeclarativa()
depurar.tree = arbol