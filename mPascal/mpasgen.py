'''
Created on 27/02/2012

@author: elfotografo007
'''
#mpasgen.py

from Visitante import Visitante
from Nodo import Nodo, NodoEstructuraFuncion, NodoArguments, NodoArg, NodoLocals,\
    NodoDeclaraciones, NodoWhile, NodoIf, NodoIfElse, NodoAsign,\
    NodoIdentificador, NodoExprList, NodoExpression, NodoTerm, NodoFactor,\
    NodoUnario, NodoExpr_And, NodoExpr_Or, NodoComparacion,NodoStmts,NodoIndex,NodoRelation,\
    NodoNumero
    

    
class VisitanteGenerar(Visitante):
    
    def __init__(self, file):
        self.file = file
    
    def generate(self, top):
        print >>self.file, "!Creado por mpascal.py"
        print >>self.file, "! Esteban Santa y Andres Torres, IS744 (2012-1)"
        self.visiteme(top)
        
    def visiteme(self, objeto):
        if isinstance(objeto, Nodo):
            if objeto.etiqueta == 'programa':
                print >>self.file, "\n! programa"
                for hoja in objeto.hojas:
                    hoja.accept(self)
                    
            if objeto.etiqueta == 'str_write':
                print >>self.file, "\n! write (start)"
                for hoja in objeto.hojas:
                    hoja.accept(self)
                print >>self.file, "!  expr := pop"
                print >>self.file, "!  write(expr)"
                print >>self.file, "! write (end)"
                
            if objeto.etiqueta == 'declaraciones_funcion':
                for hoja in objeto.hojas:
                    hoja.accept(self)
                    
            if objeto.etiqueta == 'str_read':
                print >>self.file, "\n! read (start)"
                for hoja in objeto.hojas:
                    hoja.accept(self)
                print >>self.file, "! read (end)"
            
            if objeto.etiqueta == 'str_print':
                print >>self.file, "\n! print (start)"
                for hoja in objeto.hojas:
                    hoja.accept(self)
                print >>self.file, "! print (end)"
            
            if objeto.etiqueta == 'expr_not':
                for hoja in objeto.hojas:
                    hoja.accept(self)
                    
            if objeto.etiqueta == 'llamada':
                for hoja in objeto.hojas:
                    if isinstance(hoja, NodoIdentificador):
                        print >>self.file, "! push %s()" % hoja.identificador 
                    elif isinstance(hoja, NodoExprList):
                        pass
                    hoja.accept(self)
                    

            if objeto.etiqueta == 'str_return':
                print >>self.file, "\n! return (start)"
                for hoja in objeto.hojas:
                    hoja.accept(self)
                print >>self.file, "! return (end)"
        
        elif isinstance(objeto, NodoEstructuraFuncion):
                print >>self.file, "\n! funcion %s (start)" % objeto.identificador.identificador
                if objeto.locals:
                    objeto.locals.accept(self)
                objeto.declaraciones.accept(self)
                print >>self.file, "! funcion %s (end)" % objeto.identificador.identificador
        
        elif isinstance(objeto, NodoArguments):
            if objeto.arguments:
                objeto.arguments.accept(self)
            objeto.arg.accept(self)
            
        elif isinstance(objeto, NodoArg):
            pass
        
        elif isinstance(objeto, NodoLocals):
            if objeto.locals:
                objeto.locals.accept(self)
            objeto.arg.accept(self)
            
        elif isinstance(objeto, NodoDeclaraciones) or isinstance(objeto, NodoStmts):
            if objeto.declaraciones:
                objeto.declaraciones.accept(self)
            objeto.instruccion.accept(self)
            
        elif isinstance(objeto, NodoWhile):
            print >>self.file, "\n! while (start)"
            objeto.relation.accept(self)
            objeto.stmts.accept(self)
            print >>self.file, "! while (end)"
            
        elif isinstance(objeto, NodoIf):
            print >>self.file, "\n! if (start)"
            objeto.relation.accept(self)
            objeto.stmts.accept(self)
            print >>self.file, "! if (end)"
            
        elif isinstance(objeto, NodoIfElse):
            print >>self.file, "\n! if (start)"
            objeto.relation.accept(self)
            objeto.stmts1.accept(self)
            objeto.stmts2.accept(self)
            print >>self.file, "! if (end)"
            
        elif isinstance(objeto, NodoAsign):
            print >>self.file, "\n! assign (start)"
            objeto.location.accept(self)
            objeto.expression.accept(self)
            if isinstance(objeto.expression, NodoIdentificador):
                if not objeto.expression.index:
                    print >>self.file, "!  push", objeto.expression.identificador
            print >>self.file, "!  %s := pop" % objeto.location.identificador
            print >>self.file, "! assign (end)"
            
        elif isinstance(objeto, NodoIdentificador):
            if objeto.index:
                objeto.index.accept(self)
                print >>self.file, "!  index := pop"
                print >>self.file, "!  push %s[index]" % objeto.identificador
        
        elif isinstance(objeto, NodoExprList):
            if objeto.exprlist:
                objeto.exprlist.accept(self)
            objeto.expression.accept(self)
            
        elif isinstance(objeto, NodoExpression):
            if objeto.expression:
                objeto.expression.accept(self)
                if isinstance(objeto.expression, NodoIdentificador):
                    if not objeto.expression.index:
                        print >>self.file, "!  push", objeto.expression.identificador
            objeto.term.accept(self)
            if isinstance(objeto.term, NodoIdentificador):
                if not objeto.term.index:
                    print >>self.file, "!  push", objeto.term.identificador
            if objeto.op.op == '+':
                print >>self.file, "!  add"
            else:
                print >>self.file, "!  sub"
            
        elif isinstance(objeto, NodoTerm):
            if objeto.term:
                objeto.term.accept(self)
                if isinstance(objeto.term, NodoIdentificador):
                    if not objeto.term.index:
                        print >>self.file, "!  push", objeto.term.identificador
            objeto.factor.accept(self)
            if isinstance(objeto.factor, NodoIdentificador):
                print >>self.file, "!  push", objeto.factor.identificador
            
            if objeto.op.op == '*':
                print >>self.file, "!  mul"
            else:
                print >>self.file, "!  div"
            
        elif isinstance(objeto, NodoFactor):
            objeto.expression.accept(self)
            
        elif isinstance(objeto, NodoUnario):
            objeto.expression.accept(self)

        elif isinstance(objeto, NodoExpr_Or):
            if objeto.expr_or:
                objeto.expr_or.accept(self)
            objeto.expr_and.accept(self)
            
        elif isinstance(objeto, NodoExpr_And):
            if objeto.expr_and:
                objeto.expr_and.accept(self)
            objeto.expr_not.accept(self)
            
        elif isinstance(objeto, NodoComparacion):
            objeto.expression1.accept(self)
            if isinstance(objeto.expression1, NodoIdentificador):
                    print >>self.file, "!  push", objeto.expression1.identificador
            if objeto.expression2:
                objeto.expression2.accept(self)
                if isinstance(objeto.expression2, NodoIdentificador):
                    print >>self.file, "!  push", objeto.expression2.identificador
                if objeto.op.op == '<':
                    print >>self.file, "!  lt"
                elif objeto.op.op == '>':
                    print >>self.file, "!  gt"
                elif objeto.op.op == '<=':
                    print >>self.file, "!  lte"
                elif objeto.op.op == '>=':
                    print >>self.file, "!  gte"
                elif objeto.op.op == '==':
                    print >>self.file, "!  eq"
                elif objeto.op.op == '!=':
                    print >>self.file, "!  ne"
                print >>self.file, "!  relop := pop"
                
        elif isinstance(objeto, NodoNumero):
            print >>self.file, "!  push", objeto.expression