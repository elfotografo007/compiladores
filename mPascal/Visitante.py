'''
Created on 10/02/2012

@author: elfotografo007
'''
from symtab import symtab
from Nodo import Nodo, NodoEstructuraFuncion, NodoArguments, NodoArg, NodoLocals,\
    NodoDeclaraciones, NodoWhile, NodoIf, NodoIfElse, NodoAsign,\
    NodoIdentificador, NodoExprList, NodoExpression, NodoTerm, NodoFactor,\
    NodoUnario, NodoExpr_And, NodoExpr_Or, NodoComparacion
from symbol import arglist

class Visitante(object):
    '''
    Clase Visitante
    '''
    def visiteme(self, objeto):
        pass
    
class VisitanteTabla(Visitante):
    def visiteme(self, objeto):
        if isinstance(objeto, Nodo):
            if objeto.etiqueta == 'programa':
                self.tabla = symtab()
                for hoja in objeto.hojas:
                    hoja.accept(self)
                print self.tabla.getCurrent()
            if objeto.etiqueta in ['str_write', 'declaraciones_funcion']:
                for hoja in objeto.hojas:
                    hoja.accept(self)
            if objeto.etiqueta in ['str_read', 'expr_not']:
                for hoja in objeto.hojas:
                    hoja.accept(self)
                    objeto.datatype = hoja.datatype
            if objeto.etiqueta == 'llamada':
                id = None
                count = 0
                for hoja in objeto.hojas:
                    if isinstance(hoja, NodoIdentificador):
                        id = hoja.identificador
                    elif isinstance(hoja, NodoExprList):
                        temp = hoja
                        flag2 = True
                        while flag2:
                            if isinstance(temp, NodoExprList):
                                count = count + 1
                                if temp.exprlist:
                                    temp = temp.exprlist
                                else:
                                    flag2 = False
                            else:
                                flag2 = False
                    else:
                        count = count + 1
                    hoja.accept(self)
                flag, ambito = self.tabla.existe(id)
                if flag:
                    if len(ambito[id]['arguments']) != count:
                        print 'error semantico. La funcion {0} espera {1} parametros y se le pasaron {2}'.format(id, len(ambito[id]['arguments']), count)
                if ambito[id].has_key('datatype'):
                    objeto.datatype = ambito[id]['datatype']
                
            if objeto.etiqueta == 'str_return':
                for hoja in objeto.hojas:
                    hoja.accept(self)
                    if hasattr(hoja, 'datatype'):
                        objeto.datatype = hoja.datatype
        
        elif isinstance(objeto, NodoEstructuraFuncion):
            id = objeto.identificador.identificador
            objeto.ambito = self.tabla.getCurrent()
            objeto.identificador.ambito = self.tabla.getCurrent()
            flag, ambito = self.tabla.existe(id)
            if flag:
                print 'error semantico, identificador ya declarado: %s' % id
            else:
                self.tabla.agregar(id)
                self.tabla.setAtributo(id, 'tipo', 'funcion')
                self.tabla.pushAmbito()
                argsList = []
                if objeto.arguments:
                    objeto.arguments.accept(self)
                    temp = objeto.arguments
                    flag2 = True
                    while flag2:
                        if isinstance(temp, NodoArguments):
                            argsList.append({temp.arg.identificador.identificador : temp.arg.identificador.datatype})
                            if temp.arguments:
                                temp = temp.arguments
                            else:
                                flag2 = False
                        else:
                            argsList.append({temp.identificador.identificador : temp.identificador.datatype})
                            flag2 = False
                objeto.ambito[id]['arguments'] = argsList    
                if objeto.locals:
                    objeto.locals.accept(self)
                objeto.declaraciones.accept(self)
                flag2 = True
                encontrado = False
                temp = objeto.declaraciones
                while flag2:
                    if isinstance(temp, NodoDeclaraciones):
                        if isinstance(temp.instruccion, Nodo):
                            if temp.instruccion.etiqueta == 'str_return':
                                encontrado = True
                                objeto.ambito[id]['datatype'] = temp.instruccion.datatype
                                flag2 = False
                            elif temp.declaraciones:
                                temp = temp.declaraciones
                            else:
                                flag2 = False
                        elif temp.declaraciones:
                            temp = temp.declaraciones
                    elif isinstance(temp, Nodo):
                        if temp.etiqueta == 'str_return':
                            encontrado = True
                            objeto.ambito[id]['datatype'] = temp.datatype
                            flag2 = False
                        else:
                            flag2 = False
                    else:
                        flag2 = False
                if not encontrado:
                    objeto.ambito[id]['datatype'] = 'void'
                
                print self.tabla.popAmbito()
        
        elif isinstance(objeto, NodoArguments):
            if objeto.arguments:
                objeto.arguments.accept(self)
            objeto.arg.accept(self)
        elif isinstance(objeto, NodoArg):
            id = objeto.identificador.identificador
            tipo = objeto.tipo
            objeto.identificador.datatype = tipo.tipo
            self.tabla.agregar(id)
            self.tabla.setAtributo(id, 'datatype', tipo.tipo)
            if tipo.index:
                self.tabla.setAtributo(id, 'size', tipo.index.expression)
                self.tabla.setAtributo(id, 'tipo', 'arreglo')
            else:
                self.tabla.setAtributo(id, 'tipo', 'variable')
            objeto.identificador.ambito = self.tabla.getCurrent()
        elif isinstance(objeto, NodoLocals):
            if objeto.locals:
                objeto.locals.accept(self)
            objeto.arg.accept(self)
        elif isinstance(objeto, NodoDeclaraciones):
            if objeto.declaraciones:
                objeto.declaraciones.accept(self)
            objeto.instruccion.accept(self)
        elif isinstance(objeto, NodoWhile):
            objeto.relation.accept(self)
            objeto.stmts.accept(self)
        elif isinstance(objeto, NodoIf):
            objeto.relation.accept(self)
            objeto.stmts.accept(self)
        elif isinstance(objeto, NodoIfElse):
            objeto.relation.accept(self)
            objeto.stmts1.accept(self)
            objeto.stmts2.accept(self)
        elif isinstance(objeto, NodoAsign):
            objeto.location.accept(self)
            objeto.expression.accept(self)
        elif isinstance(objeto, NodoIdentificador):
            flag, ambito = self.tabla.existe(objeto.identificador)
            if not flag:
                print 'error semantico, identificador no declarado: %s' % objeto.identificador
            else:
                if objeto.index:
                    objeto.indice = objeto.index.expression
                if ambito[objeto.identificador]['tipo'] == 'variable' or ambito[objeto.identificador]['tipo'] == 'arreglo':
                    objeto.datatype = ambito[objeto.identificador]['datatype']
        elif isinstance(objeto, NodoExprList):
            if objeto.exprlist:
                objeto.exprlist.accept(self)
            objeto.expression.accept(self)
        elif isinstance(objeto, NodoExpression):
            objeto.term.accept(self)
            if objeto.expression:
                objeto.expression.accept(self)
                if hasattr(objeto.expression, 'datatype'):
                    objeto.datatype = objeto.expression.datatype
            else:
                objeto.datatype = objeto.term.datatype
        elif isinstance(objeto, NodoTerm):
            objeto.factor.accept(self)
            if objeto.term:
                objeto.term.accept(self)
                if hasattr(objeto.term, 'datatype'):
                    objeto.datatype = objeto.term.datatype
            else:
                objeto.datatype = objeto.factor.datatype
        elif isinstance(objeto, NodoFactor):
            objeto.expression.accept(self)
            objeto.datatype = objeto.expression.datatype
        elif isinstance(objeto, NodoUnario):
            objeto.expression.accept(self)
            objeto.datatype = objeto.expression.datatype
        elif isinstance(objeto, NodoExpr_Or):
            objeto.datatype = 'bool'
            if objeto.expr_or:
                objeto.expr_or.accept(self)
            objeto.expr_and.accept(self)
        elif isinstance(objeto, NodoExpr_And):
            objeto.datatype = 'bool'
            if objeto.expr_and:
                objeto.expr_and.accept(self)
            objeto.expr_not.accept(self)
        elif isinstance(objeto, NodoComparacion):
            objeto.datatype = 'bool'
            objeto.expression1.accept(self)
            if objeto.expression2:
                objeto.expression2.accept(self)
        
                    
class VisitanteTipo(Visitante):
    def visiteme(self, objeto):
        listaReturn = []
        if isinstance(objeto, NodoComparacion): # comprueba el tipo en una expresion
            objeto.expression1.accept(self)
            objeto.expression2.accept(self)
            
            if objeto.expression1.datatype != objeto.expression2.datatype:
                print "los tipod de dato no son equivalentes"
                return
        elif isinstance(objeto, NodoExpr_Or): # comprueba que los tipos e una operacion or sean iguales
            if isinstance(objeto, NodoExpr_And): # comprueba los tipos de una exprecion and
                
                if isinstance(objeto, Nodo): # comprueba los tipos de una expresion not
                    if objeto.etiqueta == 'expr_not':
                        for hoja in objeto.hojas:
                            hoja.accept(self)
                    
                else:
                    objeto.expr_and.accept(self)# comprueba en el caso de la expresion and
                    objeto.expr_not.accept(self)
                    if objeto.expr_and.datatype != objeto.expr_not.datatype:
                        print "los tipos de dato no son equivalentes"
                        return
                
            else:
                objeto.expr_or.accept(self) # comprueba en el caso de la expresion or
                objeto.expr_and.accept(self)
                if objeto.expr_or.datatype != objeto.expr_and.datatype:
                    print "los tipos de dato no son equivalentes"
                    return
        elif isinstance(objeto, NodoExpression): # comprueba en el caso de una suma o resta
            objeto.expression.accept(self)
            objeto.term.accept(self)
            if objeto.expression.datatype != objeto.term.datatype:
                print "los tipos de dato no son equivalentes"
                return
        elif isinstance(objeto, NodoTerm):#compreba en el caso de una multiplicacion o division
            objeto.term.accept(self)
            objeto.factor.accept(self)
            if objeto.term.datatype != objeto.factor.accept(self):
                print "los tipos de dato no son equivalentes"
                return
        elif isinstance(objeto, Nodo): # comprueba el caso del return
            if objeto.etiqueta == 'str_return':
                for hoja in objeto.hojas:
                    hoja.accept(self) 
                listaReturn.append(objeto.datatype)
        elif isinstance(objeto, NodoAsign):#comprueba la asignacion
            if isinstance(objeto.location, NodoIdentificador):
                if objeto.location.index != None: # comprueba cuando la asignacion es a un vector
                    objeto.location.index.accept(self)
                    objeto.expression.accept(self)
                    if objeto.location.index.datatype != objeto.expression.datatype:
                        print "los tipos de dato no son equivalentes"
                        return
                else:
                    objeto.location.accept(self)
                    objeto.expression.accept(self)
                    if objeto.location.datatype != objeto.expression.datatype:
                        print "los tipos de dato no son equivalentes"
                        return
             
        if len(listaReturn) >= 2: # revisa la lista de returns para que sean del mismo tipo
            for elemento in listaReturn:
                if elemento != listaReturn[0]:
                    
                    print "los tiposde dato que se retornan son diferentes"
                    return
