'''
Created on 10/02/2012

@author: elfotografo007
'''
from symtab import symtab
from Nodo import Nodo, NodoEstructuraFuncion, NodoArguments, NodoArg, NodoLocals,\
    NodoDeclaraciones, NodoWhile, NodoIf, NodoIfElse, NodoAsign,\
    NodoIdentificador, NodoExprList, NodoExpression, NodoTerm, NodoFactor,\
    NodoUnario, NodoExpr_And, NodoExpr_Or, NodoComparacion,NodoStmts,NodoIndex,NodoRelation,\
    NodoNumero

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
                #print self.tabla.getCurrent()
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
                objeto.ambito = ambito
                
            if objeto.etiqueta == 'str_return':
                for hoja in objeto.hojas:
                    hoja.accept(self)
                    if hasattr(hoja, 'datatype'):
                        objeto.datatype = hoja.datatype
                    self.tabla.getCurrent()['return'].append(objeto)
        
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
                            atributosArg = {}
                            atributosArg['id'] = temp.arg.identificador.identificador
                            atributosArg['datatype']=temp.arg.identificador.datatype
                            if temp.arg.tipo.index:
                                atributosArg['tipo']= 'arreglo'
                                if isinstance(temp.arg.tipo.index, NodoNumero):
                                    atributosArg['size'] = temp.arg.tipo.index.expression
                            else:
                                atributosArg['tipo']= 'variable'
                            argsList.append(atributosArg)
                            if temp.arguments:
                                temp = temp.arguments
                            else:
                                flag2 = False
                        else:
                            atributosArg = {}
                            atributosArg['id'] = temp.identificador.identificador
                            atributosArg['datatype']= temp.identificador.datatype
                            if temp.tipo.index:
                                atributosArg['tipo']= 'arreglo'
                                if isinstance(temp.tipo.index, NodoNumero):
                                    atributosArg['size'] = temp.tipo.index.expression
                            else:
                                atributosArg['tipo']= 'variable'
                            argsList.append(atributosArg)
                            flag2 = False
                objeto.ambito[id]['arguments'] = argsList 
                self.tabla.getCurrent()['return'] = []
                if objeto.locals:
                    objeto.locals.accept(self)
                objeto.declaraciones.accept(self)
                encontrado = False
                for i in self.tabla.getCurrent()['return']:
                    if hasattr(i, 'datatype'):
                        objeto.ambito[id]['datatype'] = i.datatype
                        encontrado = True
                        break
                if not encontrado:
                    objeto.ambito[id]['datatype'] = 'void'
                del self.tabla.getCurrent()['return']
                
                objeto.locales = self.tabla.popAmbito()
        
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
        elif isinstance(objeto, NodoDeclaraciones) or isinstance(objeto, NodoStmts):
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
                    objeto.index.accept(self)
                    if isinstance(objeto.index, NodoExpression):
                        objeto.indice = objeto.index.expression
                if ambito[objeto.identificador]['tipo'] == 'variable' or ambito[objeto.identificador]['tipo'] == 'arreglo':
                    objeto.datatype = ambito[objeto.identificador]['datatype']
                objeto.ambito = ambito
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
        
        if isinstance(objeto, Nodo):
            if objeto.etiqueta == 'programa':
                for hoja in objeto.hojas:
                    hoja.accept(self)
            elif objeto.etiqueta in ['declaraciones_funcion', 'str_write']:
                for hoja in objeto.hojas:
                    hoja.accept(self)
            if objeto.etiqueta == 'str_return': 
                for hoja in objeto.hojas:
                    hoja.accept(self) 
                    if not hasattr(objeto, 'datatype'):
                        if hasattr(hoja, 'datatype'):
                            objeto.datatype = hoja.datatype
                listaReturn.append(objeto.datatype)
            elif objeto.etiqueta == 'expr_not':
                for hoja in objeto.hojas:
                        hoja.accept(self) 
            elif objeto.etiqueta == 'llamada':
                id = objeto.hojas[0].identificador
                objeto.datatype = objeto.ambito[id]['datatype']
                argList = objeto.ambito[id]['arguments']
                
                for hoja in objeto.hojas:
                    contador= 0
                    if isinstance(hoja, NodoExprList):
                        temp = hoja
                        flag2 = True
                        while flag2:
                            if isinstance(temp.expression, NodoExpression) or isinstance(temp.expression, NodoTerm) or isinstance(temp.expression, NodoFactor) or isinstance(temp.expression, NodoNumero):
                                if argList[contador]['datatype'] != temp.expression.datatype:
                                    print 'Error, se esta pasando un tipo de dato equivocado en el argumento de la funcion %s' % id
                                
                            elif isinstance(temp.expression, NodoIdentificador):
                                if argList[contador]['datatype'] != temp.expression.datatype:
                                    print 'Error, se esta pasando un tipo de dato equivocado en el argumento de la funcion %s' % id
                                ambitoId = temp.expression.ambito
                                if ambitoId[temp.expression.identificador]['tipo'] == argList[contador]['tipo']:
                                    if ambitoId[temp.expression.identificador]['tipo'] == 'arreglo':
                                        if ambitoId[temp.expression.identificador]['size'] != argList[contador]['size']:
                                            print 'Error, se esta enviando un vector de dimension {0}, y la funcion {1} espera uno de dimension {2}'.format(str(ambitoId[temp.expression.identificador]['size']), id, str(argList[contador]['size']))
                                else:
                                    print 'Error, Se esta enviando un {0}, y la funcion {1} espera {2}'.format(str(ambitoId[temp.expression.identificador]['tipo']), id, str(argList[contador]['tipo']))
                            if temp.exprlist:
                                contador+=1
                                temp = temp.exprlist
                            else:
                                flag2 = False
                                
                                    
            
        elif isinstance(objeto, NodoEstructuraFuncion):
            objeto.declaraciones.accept(self)
            if objeto.arguments:
                objeto.arguments.accept(self)
                
        elif isinstance(objeto, NodoArguments):
            objeto.arg.accept(self)
            objeto.arguments.accept(self)
        
        elif isinstance(objeto, NodoArg):
            objeto.tipo.accept(self)      
            if objeto.tipo.index:
                if objeto.tipo.index.datatype != 'int':
                    print 'Error, se esta declarando un argumento que tiene un arreglo cuyo indice no es entero'
                
            
                    
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
        elif isinstance(objeto, NodoFactor):
            objeto.expression.accept(self)
            if not hasattr(objeto, 'datatype'):
                if hasattr(objeto.expression, 'datatype'):
                    objeto.datatype = objeto.expression.datatype
        elif isinstance(objeto, NodoStmts):
            if objeto.declaraciones:
                objeto.declaraciones.accept(self)
            objeto.instruccion.accept(self)
        elif isinstance(objeto, NodoRelation):
            objeto.expression.accept(self)
            
        elif isinstance(objeto, NodoComparacion): 
            objeto.expression1.accept(self)
            if objeto.expression2:
                objeto.expression2.accept(self)
                if objeto.expression1.datatype != objeto.expression2.datatype:
                    print "los tipos de dato no son equivalentes en la comparacion"
                    return
        elif isinstance(objeto, NodoExpr_Or): 
            objeto.expr_or.accept(self) 
            objeto.expr_and.accept(self)
            if objeto.expr_or.datatype != objeto.expr_and.datatype:
                print "los tipos de dato en la expresion or no son equivalentes"
                return
        elif isinstance(objeto, NodoExpr_And):   
                objeto.expr_and.accept(self)
                objeto.expr_not.accept(self)
                if objeto.expr_and.datatype != objeto.expr_not.datatype:
                    print "los tipos de dato en la expresion and, no son equivalentes "
                    return    
        elif isinstance(objeto, NodoExpression): 
            objeto.expression.accept(self)
            objeto.term.accept(self)
            if not hasattr(objeto, 'datatype'):
                if hasattr(objeto.expression, 'datatype'):
                    objeto.datatype = objeto.expression.datatype
                elif hasattr(objeto.term, 'datatype'):
                    objeto.datatype = objeto.term.datatype
                    
            if objeto.expression.datatype != objeto.term.datatype:
                print "los tipos de dato en la expresion matematica de suma o resta no son equivalentes"
                return
        elif isinstance(objeto, NodoTerm):
            objeto.term.accept(self)
            objeto.factor.accept(self)
            if not hasattr(objeto, 'datatype'):
                if hasattr(objeto.term, 'datatype'):
                    objeto.datatype = objeto.term.datatype
                elif hasattr(objeto.factor, 'datatype'):
                    objeto.datatype = objeto.factor.datatype
                    
            if objeto.term.datatype != objeto.factor.datatype:
                print "los tipos de dato en la expresion matematica de multiplicacion o division no son equivalentes" 
                return
        elif isinstance(objeto, NodoIndex):
            if objeto.datatype != 'int':
                print "los tipos de dato en la expresion matematica de multiplicacion o division no son equivalentes"
                return
            
        elif isinstance(objeto, NodoAsign):
                   
            objeto.location.accept(self)
            objeto.expression.accept(self)
            if objeto.location.datatype != objeto.expression.datatype:
                print "los tipos de dato en la asignacion no son equivalentes"
                return
         
        if len(listaReturn) >= 2:
            for elemento in listaReturn:
                if elemento != listaReturn[0]:
                    
                    print "los tiposde dato que se retornan son diferentes"
                    return
