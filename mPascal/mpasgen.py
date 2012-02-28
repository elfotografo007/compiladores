'''
Created on 27/02/2012

@author: elfotografo007
'''
#mpasgen.py

from StringIO import StringIO
from Visitante import Visitante
from Nodo import Nodo, NodoEstructuraFuncion, NodoArguments, NodoArg, NodoLocals,\
    NodoDeclaraciones, NodoWhile, NodoIf, NodoIfElse, NodoAsign,\
    NodoIdentificador, NodoExprList, NodoExpression, NodoTerm, NodoFactor,\
    NodoUnario, NodoExpr_And, NodoExpr_Or, NodoComparacion,NodoStmts,NodoIndex,NodoRelation,\
    NodoNumero
    

    
class VisitanteGenerar(Visitante):
    
    def __init__(self, file):
        self.file = file
        self.argCount = 1
        self.data = StringIO()
        self.labelCount = 0
    
    def new_label(self):
        self.labelCount += 1
        return ".L%d" % self.labelCount
    
    def generate(self, top):
        print >>self.file, "!Creado por mpascal.py"
        print >>self.file, "! Esteban Santa y Andres Torres, IS744 (2012-1)"
        print >>self.file, '    .section ".text"'
        print >>self.data, '    .section ".data"'
        self.visiteme(top)
        print >>self.file, self.data.getvalue()
        
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
#                for hoja in objeto.hojas:
#                    hoja.accept(self)
                print >>self.file, "! read (end)"
            
            if objeto.etiqueta == 'str_print':
                print >>self.file, "\n! print (start)"
                label = self.new_label()
                hoja = objeto.hojas[0]
                if isinstance(hoja, NodoNumero):
                    print >>self.data, '{0}:  .asciiz "{1}"'.format(label, hoja.expression)
                #TODO: Acciones para el la instruccion print con un identificador
                else:
                    print >>self.data, '{0}:  .asciiz "{1}"'.format(label, hoja)
                print >>self.file, "! print (end)"
            
            if objeto.etiqueta == 'expr_not':
                for hoja in objeto.hojas:
                    hoja.accept(self)
                    
            if objeto.etiqueta == 'llamada':
                if len(objeto.hojas) > 1:
                    self.argCount = 1
                    objeto.hojas[1].accept(self)
                    if not isinstance(objeto.hojas[1], NodoExprList):
                        print >>self.file, "arg1 := pop"
                    args = ''
                    for i in range(1,self.argCount):
                        args += 'arg%d,' % i
                    print >>self.file, "!  push {0}({1})".format(objeto.hojas[0].identificador, args.rstrip(','))
                else:
                    print >>self.file, "! push %s()" % objeto.hojas[0].identificador

            if objeto.etiqueta == 'str_return':
                print >>self.file, "\n! return (start)"
#                for hoja in objeto.hojas:
#                    hoja.accept(self)
                print >>self.file, "! return (end)"
        
        elif isinstance(objeto, NodoEstructuraFuncion):
                id = objeto.identificador.identificador
                print >>self.file, "\n! funcion %s (start)" % id
                print >>self.file, "    .global ", id
                print >>self.file, "%s:" % id
                if objeto.locals:
                    objeto.locals.accept(self)
                objeto.declaraciones.accept(self)
                print >>self.file, "! funcion %s (end)" % id
        
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
            loop_label = self.new_label()
            end_loop_label = self.new_label()
            print >>self.file, "%s:"  % loop_label
            objeto.relation.accept(self)
            print >>self.file, "!  relop := pop"
            print >>self.file, "!  if not relop: goto ", end_loop_label
            objeto.stmts.accept(self)
            print >>self.file, "! goto ", loop_label
            print >>self.file, "%s:" % end_loop_label
            print >>self.file, "! while (end)"
            del loop_label
            del end_loop_label
            
        elif isinstance(objeto, NodoIf):
            print >>self.file, "\n! if (start)"
            objeto.relation.accept(self)
            end_if_label = self.new_label()
            print >>self.file, "!  relop := pop"
            print >>self.file, "!  if not relop: goto ", end_if_label
            objeto.stmts.accept(self)
            print >>self.file, "%s:" % end_if_label
            print >>self.file, "! if (end)"
            del end_if_label
            
        elif isinstance(objeto, NodoIfElse):
            print >>self.file, "\n! if (start)"
            end_if_label = self.new_label()
            else_label = self.new_label()
            objeto.relation.accept(self)
            print >>self.file, "!  relop := pop"
            print >>self.file, "!  if not relop: goto ", else_label
            objeto.stmts1.accept(self)
            print >>self.file, "!  goto ", end_if_label
            print >>self.file, "%s:" % else_label
            objeto.stmts2.accept(self)
            print >>self.file, "%s:" % end_if_label
            print >>self.file, "! if (end)"
            del end_if_label
            del else_label
            
        elif isinstance(objeto, NodoAsign):
            print >>self.file, "\n! assign (start)"
            objeto.expression.accept(self)
            print >>self.file, "!  %s := pop" % objeto.location.identificador
            print >>self.file, "! assign (end)"
            
        elif isinstance(objeto, NodoIdentificador):
            if objeto.index:
                objeto.index.accept(self)
                print >>self.file, "!  index := pop"
                print >>self.file, "!  push %s[index]" % objeto.identificador
            else:
                print >>self.file, "!  push", objeto.identificador
        
        elif isinstance(objeto, NodoExprList):
            if objeto.exprlist:
                objeto.exprlist.accept(self)
            objeto.expression.accept(self)
            print >>self.file, "!  arg%d := pop" % self.argCount
            self.argCount += 1
            
        elif isinstance(objeto, NodoExpression):
            if objeto.expression:
                objeto.expression.accept(self)               
            objeto.term.accept(self)
            if objeto.op.op == '+':
                print >>self.file, "!  add"
            else:
                print >>self.file, "!  sub"
            
        elif isinstance(objeto, NodoTerm):
            if objeto.term:
                objeto.term.accept(self)
            objeto.factor.accept(self)          
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
            print >> self.file, "!  or"
            
        elif isinstance(objeto, NodoExpr_And):
            if objeto.expr_and:
                objeto.expr_and.accept(self)
            objeto.expr_not.accept(self)
            print >> self.file, "!  and"
            
        elif isinstance(objeto, NodoComparacion):
            objeto.expression1.accept(self)
            if objeto.expression2:
                objeto.expression2.accept(self)
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
                
        elif isinstance(objeto, NodoNumero):
            print >>self.file, "!  push", objeto.expression