'''
Created on 06/01/2012

@author: elfotografo007 and esanta
'''
#mpasparse.py
#Analizador Sintactico para mPascal
from Nodo import Nodo
from pascallex import tokens


def p_programa(p):
    'programa : declaraciones_funcion'
    p[0] = p[1]

def p_declaraciones_funcion1(p):
    'declaraciones_funcion : declaraciones_funcion estructura_funcion'
    p[0] = Nodo('declaraciones_funcion', [p[1], p[2]])

def p_declaraciones_funcion2(p):
    'declaraciones_funcion : estructura_funcion'
    p[0] = p[1]


_____________________________





def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Error de sintaxis en '%s'" % p.value)
    else:
        print("Error de sintaxis al fin de linea")

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    root = yacc.parse(s)
    #if root:
        #root.imprimir(1)