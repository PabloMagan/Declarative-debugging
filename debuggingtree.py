# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 10:13:38 2016

@author: usupclab-30
"""
from enum import Enum


variables = ["l","p"]
class Arboldedepuracion(object):
    def __init__(self,funcion,argumento):
        self.f = funcion
        self.arg = argumento
        self.res = None
        self.h = list()
        self.e = State.Unasked
    
    def profundidad(self):
        L=[]
        if self.h == []:
            return 1
        else:
            for hijo in self.h:
                L.append(hijo.profundidad())
        return max(L) + 1
        
    def aniadearbol(self,otro):
        self.h.append(otro)
    
    def coords_to_tree(self,lista):
        
        """La lista son las coordenadas para
        encontrar el arbol buscado"""
        
        if lista == []:
            return self
        else:
            return self.h[lista.pop(0)].coords_to_tree(lista)
        
    def tree_to_coords(self,other,L):
        # L = []
        for i in range(len(self.h)):
            if self == other:
                L.append(i)
                break
        for i in range(len(self.h)):
            for descendent in self.h[i].descendents([]):
                if descendent == other:
                    L.append(i)
                    self.h[i].tree_to_coords(other,L)
        return L
    
    def delete_tree(self,other):
        L = self.tree_to_coords(other,[])
        if len(L) == 1:
            self.h.pop(L[0])
        else:
            self.h[L[0]].delete_tree(other)
            
    def modestados(self,estado):
        self.e = State(estado)
        for i in range(len(self.h)):
            self.h[i].modestados(estado)
            
    def weight(self):
        return len(self.descendents([]))
        
    def __str__(self):
        cadena = ""
        cadena = cadena + str(self.pintar(1))
        return cadena
            
    def pintar(self, n):
        # n = 1
        print( "\t" * n, self.f, self.arg, "->", self.res)
        for h in self.h:
            h.pintar(n + 1)

    def pintarest(self, n):
        # n = 1
        print ("\t" * n, self.f, self.arg, "->", self.res, "=>", self.e)
        for h in self.h:
            h.pintarest(n + 1)
            
    def top_down(self):
        return self.h[0]

    def divide_and_query(self):
        for descendent in self.descendents([]):
            if descendent.weight() == int(self.weight()/2):
                print (descendent)
                return descendent
            if descendent.weight() == int(self.weight()/2 + 1):
                print (descendent)
                return descendent
                

    def getBuggyNode(self):
        if self.isitright():
            return None         
        else:
            if self.e == State.Unasked :
                return self
            else:
                L = []
                for i in range(len((self.h))):
                    if not self.h[i].isitright():
                        L.append(self.h[i])
                if L == []:
                    print(self)
                    return self
                else:
                    L[0].getBuggyNode()

    def descendents(self,L):
        # L = []
        L.append(self)
        for hijo in self.h:
            hijo.descendents(L)
        return L
        
    def isitright(self):
        lista = []
        L = self.descendents([])
        for tree in L:
            lista.append(tree.e)
        for i in range(len(lista)):
            if lista[i] != State.Right:
                return False
        return True
        
class State(Enum):
    Unasked = 0
    Wrong = 1
    Right = 2

        
def quicksort(l):
    if (l == []):
        return l
    else:
        piv = l[0]
        resto = l[1:]
        l,r = partition(piv, resto)
        l = quicksort(l)
        r = quicksort(r)
#        res = l + [piv] + r
        res = l + r
        return res

def partition(p, l):
    res = ([], [])
    for elem in l:
        if elem <= p:
            res[0].append(elem)
        else:
            res[1].append(elem)
    return res

def f(x,y):
    x = h(x + 1)
    return g(4) + g(y)

def g(x):
    h(9)
    return 3

def h(x):
    3
    
import sys
import inspect
import copy
#import trace


arbol = [Arboldedepuracion("foo", None)]
me_importan = ['quicksort', 'partition']

def tracefunc(frame, event, arg, l):
      global arbol
      ret = None
      # TODO Faltaría lo de obtener el nombre de modulo y centrarnos solo en ese
      
      if event == "call" and frame.f_code.co_name in l:
          # Si no hacemos deepcopy de locals a veces sobreescribe
          n = Arboldedepuracion(frame.f_code.co_name,copy.deepcopy(inspect.getargvalues(frame).locals))
          arbol.append(n)
          ret = lambda x,y,z : tracefunc(x,y,z,l)
      elif event == "return":
          arbol[-1].res = arg
          arbol[-2].aniadearbol(arbol[-1])
          arbol = arbol[:-1]
      return ret
      
tfun = sys.gettrace()
sys.settrace(lambda x,y,z : tracefunc(x,y,z,me_importan))
quicksort([3,1,5,7,4,-1])
sys.settrace(tfun)
arbol = (arbol[0].h)[0]
#arbol.e = Estado.incorrecto
arbol.modestados(2)
arbol.h[1].h[1].e = State.Wrong
#arbol.e = State.Right
