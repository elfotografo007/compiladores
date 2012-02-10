'''
Created on 06/01/2012

@author: elfotografo007
'''
#Nodo.py
class Nodos(object):
    def accept(self, visitante):
        visitante.visiteme(self)

class Nodo(Nodos):
    def __init__(self, etiqueta = ' ', hojas = []):
        self.hojas = hojas
        self.etiqueta = etiqueta
    def agregarHoja(self, objeto):
        self.hojas.append(objeto)
    
    def imprimir(self, nivel):
        print self.etiqueta
        for i in self.hojas:
            print '  ' * (nivel + 1), '+--',
            if isinstance(i, Nodos):    
                i.imprimir(nivel + 1)
            else:
                print i

class NodoIdentificador(Nodos):
    def __init__(self, identificador, index = None):
        self.identificador = identificador
        self.index = index
    def imprimir(self, nivel):
        print 'IDENTIFICADOR', '\n', '  ' * (nivel), '   |-', self.identificador
        if self.index:
            print '  ' * nivel, '   +--', 
            self.index.imprimir(nivel + 1)

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
        if self.locals:
            self.locals.imprimir(nivel + 1)
        self.declaraciones.imprimir(nivel + 1)

class NodoArguments(Nodos):
    def __init__(self, arg, arguments = None):
        self.arg = arg
        self.arguments = arguments
    def imprimir(self, nivel, flag = True):
        if flag:
                print '  ' * (nivel) , '+--','arguments'
        if self.arguments:
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
        if flag:
                print '  ' * (nivel) , '+--','locals'
        if self.locals:
            self.locals.imprimir((nivel), False)
        print '  ' * (nivel+1) , '+--',
        self.arg.imprimir(nivel+1)
  
class NodoStmts(Nodos):
    def __init__(self, instruccion, declaraciones = None):
        self.instruccion = instruccion
        self.declaraciones = declaraciones
    def imprimir(self, nivel, flag = True):
        if self.declaraciones:
            if flag:
                print '  ' * (nivel) , '+--','stmts'
            self.declaraciones.imprimir((nivel), False)
        print '  ' * (nivel+1) , '+--',
        self.instruccion.imprimir(nivel+1)
    
class NodoDeclaraciones(Nodos):
    def __init__(self, instruccion, declaraciones = None):
        self.instruccion = instruccion
        self.declaraciones = declaraciones
    def imprimir(self, nivel, flag = True):
        if flag:
                print '  ' * (nivel) , '+--','declaraciones'
        if self.declaraciones:
            self.declaraciones.imprimir((nivel), False)
        print '  ' * (nivel+1) , '+--',
        self.instruccion.imprimir(nivel+1)
        
class NodoWhile(Nodos):
    def __init__(self, relation, stmts):
        self.relation = relation
        self.stmts = stmts
    def imprimir(self, nivel):
        print 'WHILE', '\n', '  ' * (nivel + 1) , '+--',
        self.relation.imprimir(nivel + 1)
        print '  ' * (nivel + 1) , '+--','DO'
        self.stmts.imprimir(nivel + 1)

class NodoIf(Nodos):
    def __init__(self, relation, stmts):
        self.relation = relation
        self.stmts = stmts
    def imprimir(self, nivel):
        print 'IF', '\n', '  ' * (nivel + 1) , '+--',
        self.relation.imprimir(nivel + 1)
        print '  ' * (nivel + 1) , '+--','THEN'
        self.stmts.imprimir(nivel + 1)

class NodoIfElse(Nodos):
    def __init__(self, relation, stmts1, stmts2):
        self.relation = relation
        self.stmts1 = stmts1
        self.stmts2 = stmts2
    def imprimir(self, nivel):
        print 'IF', '\n', '  ' * (nivel + 1) , '+--',
        self.relation.imprimir(nivel + 1)
        print '  ' * (nivel + 1) , '+--','THEN'
        self.stmts1.imprimir(nivel + 1)
        print '  ' * (nivel + 1) , '+--','ELSE'
        self.stmts2.imprimir(nivel + 1)

class NodoAsign(Nodos):
    def __init__(self, location, expression):
        self.location = location
        self.expression = expression
    def imprimir(self, nivel):
        print 'asign', '\n', '  ' * (nivel + 1) , '+--',
        self.location.imprimir(nivel + 1)
        print '  ' * (nivel + 1) , '+--',':=', '\n', '  ' * (nivel + 2) , '+--',
        self.expression.imprimir(nivel + 2)
        
class NodoExpression(Nodos):
    def __init__(self, term, op=None, expression=None):
        self.term = term
        self.op = op
        self.expression = expression
    def imprimir(self, nivel):
        print 'expression', '\n', '  ' * (nivel + 1) , '+--',
        if self.expression:
            self.expression.imprimir(nivel + 1)
        if self.op:
            print '  ' * nivel, '  +--', 
            self.op.imprimir(nivel + 1)
            print '  ' * (nivel + 1) , '+--',
        self.term.imprimir(nivel + 1)
    
class NodoTerm(Nodos):
    def __init__(self, factor, op=None, term=None):
        self.factor = factor
        self.op = op
        self.term = term
    def imprimir(self, nivel):
        print 'term', '\n', '  ' * (nivel + 1) , '+--',
        if self.term:
            self.term.imprimir(nivel + 1)
        if self.op:
            print '  ' * nivel, '  +--', 
            self.op.imprimir(nivel + 1)
            print '  ' * (nivel + 1) , '+--',
        self.factor.imprimir(nivel + 1)

class NodoUnario(Nodos):
    def __init__(self, op, expression):
        self.op = op
        self.expression = expression
    def imprimir(self, nivel):
        print 'NodoUnario', '\n', '  ' * (nivel + 1) , '+--', self.op, '\n', '  ' * (nivel + 2), '+--',
        self.expression.imprimir(nivel+2)
        
class NodoFactor(Nodos):
    def __init__(self, expression):
        self.expression = expression
    def imprimir(self, nivel):
        print 'factor', '\n', '  ' * (nivel + 1) , '+--',
        self.expression.imprimir(nivel+1)
        
class NodoLiteral(Nodos):
    def __init__(self, expression):
        self.expression = expression
    def imprimir(self, nivel):
        print 'literal', '\n', '  ' * (nivel + 1) , '+--',
        self.expression.imprimir(nivel+1)
        
class NodoNumero(Nodos):
    def __init__(self, expression):
        self.expression = expression
    def imprimir(self, nivel):
        print 'numero', '\n', '  ' * (nivel + 1) , '+--',
        if isinstance(self.expression, Nodos):    
            self.expression.imprimir(nivel+1)
        else:
            print self.expression
        
class NodoOperador(Nodos):
    def __init__(self, op):
        self.op = op
    def imprimir(self, nivel):
        print 'op', '\n', '  ' * (nivel + 1) , '|--', self.op
        
class NodoRelation(Nodos):
    def __init__(self, expression):
        self.expression = expression
    def imprimir(self, nivel):
        print 'relation', '\n', '  ' * (nivel + 1) , '+--',
        if isinstance(self.expression, Nodos):    
            self.expression.imprimir(nivel+1)
        else:
            print self.expression       
  
class NodoExpr_Or(Nodos):
    def __init__(self, expr_and, op=None, expr_or=None):
        self.expr_and = expr_and
        self.op = op
        self.expr_or = expr_or
    def imprimir(self, nivel):
        print 'expr_or', '\n', '  ' * (nivel + 1) , '+--',
        if self.expr_or:
            self.expr_or.imprimir(nivel + 1)
        if self.op:
            print '  ' * nivel, '  +--', 
            self.op.imprimir(nivel + 1)
            print '  ' * (nivel + 1) , '+--',
        self.expr_and.imprimir(nivel + 1)        
     
class NodoExpr_And(Nodos):
    def __init__(self, expr_not, op=None, expr_and=None):
        self.expr_not = expr_not
        self.op = op
        self.expr_and = expr_and
    def imprimir(self, nivel):
        print 'expr_and', '\n', '  ' * (nivel + 1) , '+--',
        if self.expr_and:
            self.expr_and.imprimir(nivel + 1)
        if self.op:
            print '  ' * nivel, '  +--', 
            self.op.imprimir(nivel + 1)
            print '  ' * (nivel + 1) , '+--',
        self.expr_not.imprimir(nivel + 1)      
        
class NodoComparacion(Nodos):
    def __init__(self, expression1, op=None, expression2=None):
        self.expression1 = expression1
        self.op = op
        self.expression2 = expression2
    def imprimir(self, nivel):
        print 'comparacion', '\n', '  ' * (nivel + 1) , '+--',
        self.expression1.imprimir(nivel + 1)
        if self.op:
            print '  ' * nivel, '  +--', 
            self.op.imprimir(nivel + 1)
        if self.expression2:
            print '  ' * (nivel + 1) , '+--',
            self.expression2.imprimir(nivel + 1)     
        
class NodoExprList(Nodos):
    def __init__(self, expression, exprlist = None):
        self.expression = expression
        self.exprlist = exprlist
    def imprimir(self, nivel, flag = True):
        if flag:
                print 'exprlist'
        if self.exprlist:
            self.exprlist.imprimir((nivel), False)
        print '  ' * (nivel+1) , '+--',
        self.expression.imprimir(nivel+1) 
        
class NodoConversionTipo(Nodos):
    def __init__(self, tipo, expression):
        self.tipo = tipo
        self.expression = expression
    def imprimir(self, nivel):
        print 'conversion_tipo'
        print '  ' * nivel, '   +--',
        self.tipo.imprimir(nivel + 1)
        print '  ' * nivel, '   +--', 
        self.expression.imprimir(nivel + 1)