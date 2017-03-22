# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 10:13:38 2016

@author: usupclab-30
"""
from enums import State


class Arboldedepuracion(object):
    def __init__(self,funcion,argumento):
        self.f = funcion
        self.arg = argumento
        self.res = None
        self.h = list()
        self.e = State.UNASKED
        self.w = self.update_weight()
        # TODO: Sería interesante un atributo que guardase el tamaño del nodo (todos los nodos unasked que cuelgan + 1 si el nodo está unasked o nada si tiene "color")
        # Se calcula al principio y se recalcula cuando se colorea.

    def equals(self,other):
        return self.f == other.f and self.arg == other.arg

    def update_weight(self):
        if self.h == []:
            self.w = 1
        else:
            for child in self.h:
                self.w = self.w + child.update_weight()
        
    
    def depth(self):
        L=[]
        if self.h == []:
            return 1
        else:
            for hijo in self.h:
                L.append(hijo.depth())
        return max(L) + 1


    def add_tree(self,otro):
        self.h.append(otro)
    
    # TODO: Comentarios en el formato del fichero de estilo
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
                # TODO: Hacer bucle while en vez de break
                break
        for i in range(len(self.h)):
            for descendent in self.h[i].descendents([]):
                if descendent == other:
                    L.append(i)
                    self.h[i].tree_to_coords(other,L)
        return L
    
    # TODO: Comentarios en formato adecuado.
    def colour_tree(self,other,state):
        if self.equals(other):
            self.e = state
        else:
            for child in self.h:
                child.colour_tree(other,state)
        
    # TODO: Esta función modifica el estado de todos los nodos? por qué?
    """
    La ulilizo para modificar el arbol mas facilmente y hacer pruebas luego
    con las otras funciones, pero cuando ya no la necesite la quitare
    """
    def modestados(self,estado):
        self.e = State(estado)
        for child in self.h:
            child.modestados(estado)

            
#    def weightaux(self,k): #### TODO: HACER ABAJO SIN ACUMULADOR! NO ES NECESARIO GASTAR MEMORIA ADICIONAL
#        for child in self.h:
#            if child.e == State.UNASKED:
#                k = k + 1
#                child.weightaux(k)
#        return k + 1
                                    
    
    def weightaux(self,l): #### TODO: HACER ABAJO SIN ACUMULADOR! NO ES NECESARIO GASTAR MEMORIA ADICIONAL
        for child in self.h:
            if child.e == State.UNASKED:
                l.append(1)
                child.weightaux(l)
        return len(l) + 1
        
    def weight(self):
        return self.weightaux([])
        
    def __str__(self):
        cadena = ""
        cadena = cadena + str(self.pintar(1))
        return cadena
    
    def pintar(self, n):
        print( "\t" * n, self.f, self.arg, "->", self.res)
        for h in self.h:
            h.pintar(n + 1)

    def pintarest(self, n):
        # n = 1
        print ("\t" * n, self.f, self.arg, "->", self.res, "=>", self.e)
        for h in self.h:
            h.pintarest(n + 1)

    # TODO: Cambiar.
    # Ahora top down es complicado, porque hay que hacer lo siguiente: 
    # Bucar el nodo rojo con el subárbol más pequeño.
    # Preguntar por el primer hijo que no esté preguntado.
    # Nótese que esto funciona porque tenemos una precondición: el árbol no
    # tiene nodos buggy (aclarar en comentarios de la función).
    def top_down(self):
        i = 0
        while self.h[i].e != State.UNASKED and i < len(self.h):
            i = i + 1
        return self.h[i]

    def divide_and_query(self):
        node = self.weight()/2
        dif = sys.maxsize  #### TODO: USAR 'sys.maxsize'
        for child in self.descendents([]):
            if abs(node - child.weight()) < dif:
                dif = abs(node - child.weight()) #### TODO: MEJOR UNA FUNCION update_weight() QUE ACTUALIZA EL PESO DE TODOS LOS NODOS Y LO ALMACENA EN UN ATRIBUTO DE CADA NODO
        i = 0
        while abs(node - self.descendents([])[i].weight()) != dif:
            i = i + 1
        return self.descendents([])[i]
                
    def getBuggyNode(self):
        buggy = None
        if self.e == State.WRONG and self.are_childs_right():
            buggy = self
            print(self)
        else:
            for child in self.h: #### TODO: NO HAY QUE RECORRER SIEMPRE TODOS LOS HIJOS, UNICAMENTE MIENTRAS NO SE HAYA ENCONTRADO EL NODO BUGGY
                child.getBuggyNode() #### TODO: Y LO QUE DEVUELVE CADA LLAMADA RECURSIVA DONDE LO GUARDAS? NORMAL QUE SIEMPRE DEVUELVAS None, PORQUE NO PROPAGAS LO QUE ENCUENTRAS EN LOS HIJOS
        return buggy
                
            

    def descendents(self,L):
        # L = []
        L.append(self)
        for hijo in self.h:
            if hijo.e == State.UNASKED:
                hijo.descendents(L)
        return L

    def isitright(self):
        lista = []
        L = self.descendents([])
        for tree in L:
            lista.append(tree.e)
        for i in range(len(lista)):
            if lista[i] != State.RIGHT:
                return False
        return True
        
    def are_childs_right(self):
        ans = True
        i = 0
        while i < len(self.h) and ans:
            if self.h[i].e != State.RIGHT:
                ans = False
            i = i + 1
        return ans
            

        
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

variables = ["l","p"]
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
          arbol[-2].add_tree(arbol[-1])
          arbol = arbol[:-1]
      return ret
      
tfun = sys.gettrace()
sys.settrace(lambda x,y,z : tracefunc(x,y,z,me_importan))
#quicksort([3,1,5,7,4,-1])
exec("quicksort([3,1,5,7,4,-1])") #Enrique: esto ayudará a lanzar la depuración con cualquier objetivo
sys.settrace(tfun)
arbol = (arbol[0].h)[0]
arbol.pintar(0)
#arbol.e = Estado.incorrecto
arbol.modestados(0)
arbol.h[1].h[1].h[1].e = State.RIGHT
arbol.h[1].h[1].h[2].e = State.RIGHT
arbol.h[1].h[1].e = State.WRONG
arbol.h[1].h[1].h[0].e = State.RIGHT
arbol.h[2].e = State.RIGHT
arbol.modestados(0)
