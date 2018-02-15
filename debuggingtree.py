# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 10:13:38 2016

@author: Pablo Magan Hernandez
"""
from enums import State


class DebuggingTree(object):
    def __init__(self, function, arguments, out):
        self.fun = function
        self.arg = arguments
        self.out = out
        self.ret = None
        self.child = list()
        self.state = State.UNASKED
        self.weight = 1


    def equals(self,other):
        """
        Given two class objects this function returns a boolean saying if
        they are equals or not.
        
        Parameters
        ----------
        self: (DebuggingTree) First tree.
        other: (DebuggingTree) Second tree.
        
        Returns
        -------
        Bool 
            If they are equals or not.
        """
        return self.fun == other.fun and self.arg == other.arg
    
    
    def update_weight(self):
        
        """
        This function update the weight of the tree. It will be called each
        time that you modifies one state in tree.
        
        Parameters
        ----------
        self: (DebuggingTree) The tree to update his weight.
        
        Returns
        -------
        None
        Just modifies the self.weight parameter in the tree.
        """
        
        total_children = 0
        for child in self.child:
            child.update_weight()
            total_children = total_children + child.weight
        myself = 0
        if self.state == State.UNASKED:
            myself = 1
        self.weight = total_children + myself
        if self.state == State.RIGHT:
            self.weight = 0


    def add_tree(self,other):
                
        """
        This function add a new tree as child of the current tree
        
        Parameters
        ----------
        self: (DebuggingTree) The main tree.
        other: (DebuggingTree) The tree to add.
        
        Returns
        -------
        None
        Just modifies the main tree.
        """
        
        self.child.append(other)

        
    def colour_tree(self,other,state):
        
        """
        This function modifies the state in one node and with a state given.
        It will be used for modifies the tree when it recieves an answer from
        the client.
        
        Parameters
        ----------
        self: (DebuggingTree) The main tree.
        other: (DebuggingTree) The tree that the function look for in the
               main tree to modifies the state.
        state:(State) The new state for the node.
        
        Returns
        -------
        None
        Just modifies the tree.
        """
        
        if self.equals(other):
            self.state = state
        else:
            for child in self.child:
                child.colour_tree(other,state)

    def clean_tree(self):
        
        """
        This function clean the self.out param in the tree because when it was
        created, it had some extra information that we dont need.
        
        Parameters
        ----------
        self: (DebuggingTree) The main tree.
        
        Returns
        -------
        None
        Just modifies the tree.
        """
        
        aux_dict = dict()
        for i in self.out:
            if i in self.arg:
                aux_dict[i] = self.out[i]
        self.out = aux_dict
        for child in self.child:
            child.clean_tree()

    def is_compresed(self):
        b = True
        fun = self.fun
        i = 0
        while i < len(self.child):
            if self.child[i].fun == fun:
                b = False
                break
            i = i+1
        for child in self.child:
            b = b and child.is_compresed()
        return b
        

       
    def tree_compression(self):
        i = 0
        while i < len(self.child):
            if self.child[i].fun == self.fun:
                grandchildren = self.child[i].child
                self.child.pop(i)
                self.child = self.child + grandchildren
                break
            i = i+1
        if not self.is_compresed():
            self.tree_compression()
                
                
    
    def __str__(self):
        cadena = ""
        cadena = cadena + str(self.paint(1))
        return cadena
    
    def paint(self, n):
        print( "\t" * n, self.fun, self.arg, "->", self.ret)
        for child in self.child:
            child.paint(n + 1)

    def paint_state(self, n):
        # n = 1
        print ("\t" * n, self.fun, self.arg, "->", self.ret, "=>", self.state, "->", self.out)
        for child in self.child:
            child.paint_state(n + 1)

    # TODO: Cambiar.
    # Ahora top down es complicado, porque hay que hacer lo siguiente: 
    # Bucar el nodo rojo con el subárbol más pequeño.
    # Preguntar por el primer hijo que no esté preguntado.
    # Nótese que esto funciona porque tenemos una precondición: el árbol no
    # tiene nodos buggy (aclarar en comentarios de la función).
                    
    def search_smallest(self):
        
        """
        This function look for the smallest wrong sub-tree in the tree given.
        
        Parameters
        ----------
        self: (DebuggingTree) The main tree.
        
        Returns
        -------
        DebuggingTree
        Is the smallest sub-tree with wrong state.
        """
        
        if self.state == State.WRONG:
            small = (self,self.weight)
        else:
            small = (None,sys.maxsize)
        for child in self.child:
            small_child = child.search_smallest()
            if small_child[1] < small[1]:
                small = small_child
        return small
                    

    def top_down_aux(self):
        
        """
        This is an auxiliary function to look for the node to ask in the tree 
        given. It is chosen by the method top down.
        
        Parameters
        ----------
        self: (DebuggingTree) The main tree.
        
        Returns
        -------
        DebuggingTree
        The node chosen by the top down method.
        """
        
        i = 0
        while self.child[i].state != State.UNASKED and i < len(self.child):
            i = i + 1
        return self.child[i]
    
    
    def top_down(self):
        aux = self.search_smallest()[0]
        return aux.top_down_aux()
        
 
    def top_down_heaviest_first_aux(self):
        
        """
        This is an auxiliary function to look for the node to ask in the tree 
        given. It is chosen by the method top down heaviest first.
        
        Parameters
        ----------
        self: (DebuggingTree) The main tree.
        
        Returns
        -------
        DebuggingTree
        The node chosen by the top down heaviest first method.
        """
        
        maximun = (None,-sys.maxsize)
        for child in self.child:
            if child.state == State.UNASKED and child.weight > maximun[1]:
                maximun = (child,child.weight)
        return maximun[0]
        
  
    
    def top_down_heaviest_first(self):
        aux = self.search_smallest()[0]
        return aux.top_down_heaviest_first_aux()

    
    def divide_and_query_aux(self, weight):
        
        """
        This is an auxiliary function to look for the node to ask in the tree 
        given. It is chosen by the method divide and query.
        
        Parameters
        ----------
        self: (DebuggingTree) The main tree.
        
        Returns
        -------
        DebuggingTree
        The node chosen by the divide and query method.
        """
        
        if self.state == State.UNASKED:
            divide = (self,abs(self.weight - weight))
        else:
            divide = (None,sys.maxsize)
        for child in self.child:
            small_child = child.divide_and_query_aux(weight)
            if small_child[1] < divide[1]:
                divide = small_child
        return divide
    
    
    def divide_and_query(self):
        aux = self.search_smallest()[0]
        return aux.divide_and_query_aux(aux.weight/2.0)[0]
    
            
    def getBuggyNode(self):
        buggy  = None
        if self.state == State.WRONG and self.are_children_right():
            buggy = self
        else:
            buggy_child = None
            i = 0
            while i < len(self.child) and buggy_child == None:
                current = self.child[i]
                buggy_child = current.getBuggyNode()
                if buggy_child != None:
                    buggy = buggy_child
                i = i + 1
        return buggy

        
    def are_children_right(self):
        ans = True
        i = 0
        while i < len(self.child) and ans:
            if self.child[i].state != State.RIGHT:
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
        if leq(elem,p):
            res[0].append(elem)
        else:
            res[1].append(elem)
    l.append(1)
    return res

def leq(a,b):
    return a <= b   

def suma(a,b):
    return a*b

def fibonacci(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return suma(fibonacci(n-2),fibonacci(n-1))




def prueba(lista):
    a = lista[0]
    lista.pop(0)
    return a

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

tree = [DebuggingTree("foo", None, None)]
me_importan = ['quicksort', 'partition','leq']
#me_importan = ['prueba']
#me_importan = ['suma','fibonacci']

def tracefunc(frame, event, arg, l):
    
      global tree
      ret = None 
      
      if event == "call" and frame.f_code.co_name in l:
          # Si no hacemos deepcopy de locals a veces sobreescribe
          n = DebuggingTree(frame.f_code.co_name,copy.deepcopy(inspect.getargvalues(frame).locals),None)
          tree.append(n)
          ret = lambda x,y,z : tracefunc(x,y,z,l)
      elif event == "return":
          tree[-1].ret = arg
          tree[-1].out = inspect.getargvalues(frame).locals
          tree[-2].add_tree(tree[-1])
          tree = tree[:-1]
      return ret



      
tfun = sys.gettrace()
sys.settrace(lambda x,y,z : tracefunc(x,y,z,me_importan))
#quicksort([3,1,5,7,4,-1])
exec("quicksort([3,7,4,-1])")
#exec("prueba([3,1,5,7,4,-1])")
#exec("fibonacci(3)")
sys.settrace(tfun)
tree = (tree[0].child)[0]
tree.update_weight()
tree.state = State.WRONG
tree.clean_tree()
#arbol.h[1].h[1].h[1].e = State.RIGHT
#arbol.h[1].h[1].h[2].e = State.RIGHT
#arbol.h[1].h[1].e = State.WRONG
#arbol.h[1].h[1].h[0].e = State.RIGHT
#arbol.h[2].e = State.RIGHT
tree.paint_state(0)