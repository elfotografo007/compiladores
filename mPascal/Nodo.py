'''
Created on 06/01/2012

@author: elfotografo007
'''
class Nodos(object):
    pass

class Nodo(Nodos):
    def __init__(self, etiqueta = ' ', hojas = []):
        self.hojas = hojas
        self.etiqueta = etiqueta
    def agregarHoja(self, objeto):
        self.hojas.append(objeto)
    
    def imprimir(self, nivel):
        print self.etiqueta
        for i in self.hojas:
            print '  ' * nivel, '+--',
            if isinstance(i, Nodos):    
                i.imprimir(nivel + 1)
            else:
                print i

class NodoIdentificador(Nodos):
    def __init__(self, identificador):
        self.identificador = identificador
    def imprimir(self, nivel):
        print 'IDENTIFICADOR', '\n', '  ' * (nivel), '   |-', self.identificador

class NodoEstructuraFuncion(Nodos):
    def __init__(self, identificador, locals, declaraciones, arguments = None):
        self.identificador = identificador
        self.arguments = arguments
        self.locals = locals
        self.declaraciones = declaraciones
    
    def imprimir(self, nivel = 1):
        print 'estructura_funcion', '\n', '  ' * (nivel + 1) , '+--',
        self.identificador.imprimir(nivel + 1)
        if self.arguments:
            self.arguments.imprimir(nivel + 1)
        self.locals.imprimir(nivel + 1)
        self.declaraciones.imprimir(nivel + 1)

class NodoArguments(Nodos):
    def __init__(self, arg, arguments = None):
        self.arg = arg
        self.arguments = arguments
    def imprimir(self, nivel, flag = True):
        if self.arguments:
            if flag:
                print '  ' * (nivel) , '+--','arguments'
            self.arguments.imprimir((nivel), False)
        print '  ' * (nivel+1) , '+--',
        self.arg.imprimir(nivel+1)
        
class NodoArg(Nodos):
    def __init__(self, identificador, tipo):
        self.identificador = identificador
        self.tipo = tipo
    def imprimir(self, nivel):
        print 'arg', '\n','  ' * (nivel+ 1), '+--', 
        self.identificador.imprimir(nivel)
        print '  ' * (nivel+1), '+--', 
        self.tipo.imprimir(nivel+1)
        
class NodoTipo(Nodos):
    def __init__(self, tipo, index = None):
        self.tipo = tipo
        self.index = index
    def imprimir(self, nivel):
        print 'tipo', '\n', '  ' * nivel, '   |-', self.tipo
        if self.index:
            print '  ' * nivel, '   +--', 
            self.index.imprimir(nivel + 1)

class NodoIndex(Nodos):
    def __init__(self, index):
        self.index = index
    def imprimir(self, nivel):
        if isinstance(self.index, Nodos):
            print 'index', '\n','  ' * nivel, '+--',
            self.index.imprimir(nivel +1)
        else:
            print 'index', '\n','  ' * (nivel + 1) , '  ','|-',
            print self.index
            
class NodoLocals(Nodos):
    def __init__(self, arg, locals = None):
        self.arg = arg
        self.locals = locals
    def imprimir(self, nivel, flag = True):
        if self.locals:
            if flag:
                print '  ' * (nivel) , '+--','locals'
            self.locals.imprimir((nivel), False)
        print '  ' * (nivel+1) , '+--',
        self.arg.imprimir(nivel+1)
    
class NodoDeclaraciones(Nodos):
    def __init__(self, instruccion, declaraciones = None):
        self.instruccion = instruccion
        self.declaraciones = declaraciones
    def imprimir(self, nivel, flag = True):
        if self.declaraciones:
            if flag:
                print '  ' * (nivel) , '+--','declaraciones'
            self.declaraciones.imprimir((nivel), False)
        print '  ' * (nivel+1) , '+--',
        self.instruccion.imprimir(nivel+1)