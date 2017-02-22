# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 10:13:38 2016

@author: usupclab-30
"""

def elemlista(lista,elemento):
    for i in range(len(lista)):
        if lista[i]==elemento:
            return True
            
variables = ["x","y","z"]
class Arboldedepuracion(object):
    def __init__(self,funcion,argumento):
        self.f = funcion
        self.arg = argumento
        self.res = None
        self.h = list()
        self.e = 0 # 0 para incorrecto y 1 para correcto.
    
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

    def modestados(self,estado):
        self.e = estado
        for i in range(len(self.h)):
            self.h[i].modestados(estado)
        
    def __str__(self):
        cadena = ""
        cadena = cadena + str(self.pintar(1))
        return cadena
            
    def pintar(self, n):
        print "\t" * n, self.f, self.arg, "->", self.res
        for h in self.h:
            h.pintar(n + 1)
                
def top_down(arbol):
    for i in range(len(arbol.h)):
        print arbol.h[i].f,arbol.h[i].arg,"->",arbol.h[i].res
        respuesta = raw_input(" ¿Es eso correcto?: ")
        if respuesta == "si":
            arbol.h[i].modestados(1)
        else:
            top_down(arbol.h[i])

            
def bug (arbol):
    for i in range(len(arbol.h)):
        if arbol.h[i].e == 1:
            None
        else:
            if arbol.h[i].h == []:
                return arbol.h[i].f,arbol.h[i].arg,"->",arbol.h[i].res
            else:
                bug(arbol.h[i])
                
            

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
me_importan = ['f', 'g', 'h']

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
f(3, 1)
sys.settrace(tfun)
arbol = (arbol[0].h)[0]
#arbol.e = Estado.incorrecto