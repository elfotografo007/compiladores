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

def p_estructura_funcion1(p):
    "estructura_funcion : FUN IDENTIFICADOR '(' arguments ')' locals BEGIN declaraciones END"
    p[0] = Nodo('estructura_funcion', [p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9]])

def p_estructura_funcion2(p):
    "estructura_funcion : FUN IDENTIFICADOR '(' ')' locals BEGIN declaraciones END"
    p[0] = Nodo('estructura_funcion', [p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]])

def p_arguments1(p):
    "arguments : arguments ',' arg"
    p[0] = Nodo('arguments',[p[1], p[2]])
    
def p_arguments2(p):
    'arguments : arg'
    p[0] = p[1]

def p_arg(p):
    "arg : IDENTIFICADOR ':' tipo"
    p[0] = Nodo('arg', [p[1], p[2], p[3]])

def p_locals1(p):
    'locals : empty'
    p[0] = p[1]
    
def p_locals2(p):
    "locals : locals arg ';'"
    p[0] = Nodo('locals', [p[1], p[2], p[3]])

def p_locals3(p):
    "locals : locals declaraciones_funcion ';'"
    p[0] = Nodo('locals', [p[1], p[2], p[3]])

def p_locals4(p):
    "locals : arg ';'"
    p[0] = Nodo('locals', [p[1], p[2]])

def p_locals5(p):
    "locals : declaraciones_funcion ';'"
    p[0] = Nodo('locals', [p[1], p[2]])

def p_tipo1(p):
    'tipo : INT'
    p[0] = p[1]
    
def p_tipo2(p):
    'tipo : FLOAT'
    p[0] = p[1]

def p_tipo3(p):
    "tipo : INT '[' index ']'"
    p[0] = Nodo('tipo', [p[1], p[2], p[3], p[4]])
    
def p_tipo4(p):
    "tipo : FLOAT '[' index ']'"
    p[0] = Nodo('tipo', [p[1], p[2], p[3], p[4]])

def p_stmts1(p):
    "stmts : BEGIN declaraciones ';' instruccion END"
    p[0] = Nodo('estructura_funcion', [p[0], p[1], p[2], p[3], p[4], p[5]])

def p_stmts2(p):
    'stmts : instruccion'
    p[0] = p[1]

def p_declaraciones1(p):
    "declaraciones : declaraciones ';' instruccion"
    p[0] = Nodo('declaraciones', [p[1], p[2], p[3]])

def p_declaraciones2(p):
    'declaraciones : instruccion'
    p[0] = p[1]

def p_instruccion1(p):
    "instruccion : str_while"
    p[0] = p[1]
    
def p_instruccion2(p):
    "instruccion : str_if"
    p[0] = p[1]

def p_instruccion3(p):
    "instruccion : str_if_else"
    p[0] = p[1]

def p_instruccion4(p):
    "instruccion : asign"
    p[0] = p[1]

def p_instruccion5(p):
    "instruccion : str_print"
    p[0] = p[1]
    
def p_instruccion6(p):
    "instruccion : str_write"
    p[0] = p[1]

def p_instruccion7(p):
    "instruccion : str_read"
    p[0] = p[1]

def p_instruccion8(p):
    "instruccion : str_return"
    p[0] = p[1]

def p_instruccion9(p):
    "instruccion : llamada"
    p[0] = p[1]

def p_instruccion10(p):
    "instruccion : SKIP"
    p[0] = p[1]

def p_instruccion11(p):
    "instruccion : BREAK"
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