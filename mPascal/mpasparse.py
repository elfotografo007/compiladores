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

def p_str_while(p):
    'str_while : WHILE relation DO stmts'
    p[0]=Nodo('str_while',[p[1],p[2],p[3],p[4]])

def p_str_if(p):
    'str_if : IF relation THEN stmts'
    p[0]=Nodo('str_if',[p[1],p[2],p[3],p[4]])

def p_str_if_else(p):
    'str_if_else : IF relation THEN stmts ELSE stmts'
    p[0]=Nodo('str_if',[p[1],p[2],p[3],p[4],p[5],p[6]])

def p_asign(p):
    'asign : location ASIGNACION expression'
    p[0]=Nodo('asign',[p[1],p[2],p[3]])

def p_str_print(p):
    "str_print : PRINT '(' literal ')'"
    p[0]=Nodo('str_print',[p[1],p[2],p[3],p[4]])
    
def p_str_write(p):
    "str_write : WRITE '(' expression ')'"
    p[0]=Nodo('str_write',[p[1],p[2],p[3],p[4]])

def p_str_read(p):
    "str_read : READ '(' location ')'"
    p[0]=Nodo('str_read',[p[1],p[2],p[3],p[4]])
    
def p_str_return(p):
    'str_return : RETURN expression'
    p[0]=Nodo('str_return',p[1],p[2])

def p_llamada1(p):
    "llamada : IDENTIFICADOR '(' exprlist ')' "
    p[0]=Nodo('llamada',[p[1],p[2],p[3],p[4]])

def p_llamada2(p):
    "llamada : IDENTIFICADOR '(' ')'"
    p[0]=Nodo('llamada',[p[1],p[2],p[3]])
    
def p_relation1(p):
    'relation1 : expression oprel expression'
    p[0]=Nodo('relation',[p[1],p[2],p[3]])
    
def p_relation2(p):
    'relation : relation AND relation'
    p[0]=Nodo('relation',[p[1],p[2],p[3]])
    
def p_relation3(p):
    'relation : NOT relation'
    p[0]=Nodo('relation',[p[1],p[2]])

def p_relation4(p):
    'relation : relation OR relation'
    p[0]=Nodo('relation',[p[1],p[2],p[3]])
    
def p_relation5(p):
    "relation : '(' relation ')'"
    p[0]=Nodo('relation',[p[1],p[2],p[3]])
    
def p_oprel1(p):
    "oprel : '<'"
    p[0]=p[1]

def p_oprel2(p):
    "oprel : '>'"
    p[0]=p[1]

def p_oprel3(p):
    'oprel : MENORIGUAL'
    p[0]=p[1]

def p_oprel4(p):
    'oprel : MAYOUIGUAL'
    p[0]=p[1]
    
def p_oprel5(p):
    'oprel : IGUALIGUAL'
    p[0]=p[1]
    
def p_oprel6(p):
    'oprel : DIFERENTE'
    p[0]=p[1]
    
def p_exprlist1(p):
    "exprlist : exprlist ',' expression"
    p[0]=Nodo('exprlist',[p[1],p[2],p[3]])
    
def p_exprlist2(p):
    'exprlist : expression'
    p[0]=p[1]
      
def p_expression1(p):
    'expression : expression opsuma term'    
    p[0]=Nodo('expression',[p[1],p[2],p[3]])
    
def p_expression2(p):
    'expression : expression opsuma term'    
    p[0]=p[1]

def p_opsuma1(p):
    "opsuma : '+'"
    p[0]=p[1]

def p_opsuma2(p):
    "opsuma : '-'"
    p[0]=p[1]

def p_term1(p):
    'term: term opmult factor'    
    p[0]=Nodo('term',[p[1],p[2],p[3]])
    
def p_term2(p):
    'term: factor'    
    p[0]=p[1]
    
def p_opmult1(p):
    "opmult: '*'"
    p[0]=p[1]
    
def p_opmult2(p):
    "opmult: '/'"
    p[0]=p[1]
    
def p_factor1(p):
    "factor : '('expression')'"
    p[0]=Nodo('factor',[p[1],p[2],p[3]])
    
def p_factor2(p):
    'factor : numero'
    p[0]=p[1]
    
def p_factor3(p):
    "factor : '-'expression"
    p[0]=Nodo('factor',[p[1],p[2]])

def p_factor4(p):
    "factor : '+'expression"
    p[0]=Nodo('factor',[p[1],p[2]])
    
def p_factor5(p):
    'factor : llamada'
    p[0]=p[1]
    
def p_factor6(p):
    'factor : location'
    p[0]=p[1]
    
def p_location1(p):
    'location : IDENTIFICADOR'
    p[0]=p[1]
    
def p_location2(p):
    "location : IDENTIFICADOR'['index']'"
    p[0]=Nodo('location',[p[1],p[2],p[3],p[4]])

def p_index1(p):
    'index : expression'
    p[0]=p[1]
    
def p_index2(p):
    'index : ENTERO'
    p[0]=p[1]
    
def p_literal1(p):
    'literal : IDENTIFICADOR'
    p[0]=p[1]

def p_literal2(p):
    'literal : numero'
    p[0]=p[1]        

def p_literal3(p):
    'literal : STRING'
    p[0]=p[1]
    
def p_numero1(p):
    'numero : ENTERO'
    p[0]=p[1]

def p_numero2(p):
    'numero : FLOTANTE'
    p[0]=p[1]
    
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
