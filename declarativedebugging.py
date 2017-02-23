# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:52:12 2017

@author: adrian
"""

class DepuracionDeclarativa(object):
    def __init__(self):
        self.strategy = 0 # 0 top-down 1 divide-and-query
        self.undo_list = []
        self.arbol = None
        
    def depuracion_declarativa(self):
        while self.arbol.getBuggyNode() != None:
            self.ask()
    
    def ask(self):
        # Hacer copia del arbol
        # Guardar en la lista
        if self.strategy == 0:
            nodo = self.arbol.top_down()
        elif self.strategy == 1:
            nodo = self.arbol.divide_and_query()
        
        print(nodo.f, nodo.arg,"->", nodo.res)
        respuesta = raw_input(" ¿Es eso correcto?: ")
        if respuesta == "yes":
            pass
        elif respuesta == "no":
            self.arbol = nodo
        elif respuesta == "undo":
            pass