'''
Created on 06/01/2012

@author: elfotografo007 and esanta
'''
#mpasparse.py
#Analizador Sintactico para mPascal
from Nodo import Nodo, NodoEstructuraFuncion, NodoIdentificador, NodoArguments,\
    NodoArg, NodoTipo, NodoIndex, NodoLocals, NodoDeclaraciones, NodoStmts,\
    NodoWhile, NodoIf, NodoIfElse, NodoAsign, NodoExpression, NodoTerm,\
    NodoFactor, NodoUnario, NodoLiteral, NodoNumero, NodoOperador, NodoExpr_Or,\
    NodoExpr_And, NodoComparacion, NodoRelation, NodoExprList,\
    NodoConversionTipo
from pascallex import tokens
from Visitante import VisitanteTabla, VisitanteTipo

precedence = (
       ('left', '+', '-'),
       ('left', '*', '/'),
       ('right', 'UMINUS'),
       ('right', 'UPLUS'),
       ('right', 'NOT'),
       ('left', '(', ')'),
       ('left', '[', ']'),
       ('right', 'ASIGNACION')
             )

def p_programa(p):
    'programa : declaraciones_funcion'
    p[0] = Nodo('programa', [p[1]])


def p_declaraciones_funcion1(p):
    'declaraciones_funcion : declaraciones_funcion estructura_funcion'
    p[0] = Nodo('declaraciones_funcion', [p[1], p[2]])

def p_declaraciones_funcion2(p):
    'declaraciones_funcion : estructura_funcion'
    p[0] = p[1]

def p_estructura_funcion1(p):
    "estructura_funcion : FUN IDENTIFICADOR '(' arguments ')' locals BEGIN declaraciones END"
    p[0] = NodoEstructuraFuncion(identificador = NodoIdentificador(p[2]), arguments = p[4], locals =p[6], declaraciones = p[8])

def p_estructura_funcion2(p):
    "estructura_funcion : FUN IDENTIFICADOR '(' ')' locals BEGIN declaraciones END"
    p[0] = NodoEstructuraFuncion(identificador = NodoIdentificador(p[2]), locals = p[5], declaraciones = p[7])

def p_arguments1(p):
    "arguments : arguments ',' arg"
    p[0] = NodoArguments(p[3], p[1])
    
def p_arguments2(p):
    'arguments : arg'
    p[0] = p[1]

def p_arg(p):
    "arg : IDENTIFICADOR ':' tipo"
    p[0] = NodoArg(NodoIdentificador(p[1]), p[3])

def p_locals1(p):
    'locals : empty'
    p[0] = p[1]
    
def p_locals2(p):
    "locals : locals arg ';'"
    p[0] = NodoLocals(p[2], p[1])

def p_locals3(p):
    "locals : locals declaraciones_funcion ';'"
    p[0] = NodoLocals(p[2], p[1])

def p_locals4(p):
    "locals : arg ';'"
    p[0] = NodoLocals(p[1])

def p_locals5(p):
    "locals : declaraciones_funcion ';'"
    p[0] = NodoLocals(p[1])

def p_tipo1(p):
    'tipo : INT'
    p[0] = NodoTipo(p[1])
    
def p_tipo2(p):
    'tipo : FLOAT'
    p[0] = NodoTipo(p[1])

def p_tipo3(p):
    "tipo : INT '[' index ']'"
    p[0] = NodoTipo(p[1], p[3])
    
def p_tipo4(p):
    "tipo : FLOAT '[' index ']'"
    p[0] = NodoTipo(p[1], p[3])

def p_stmts1(p):
    "stmts : BEGIN declaraciones ';' instruccion END"
    p[0] = NodoStmts(p[4], p[2])

def p_stmts2(p):
    'stmts : instruccion'
    p[0] = p[1]

def p_declaraciones1(p):
    "declaraciones : declaraciones ';' instruccion"
    p[0] = NodoDeclaraciones(p[3], p[1])

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
    p[0] = Nodo('skip', [p[1]])

def p_instruccion11(p):
    "instruccion : BREAK"
    p[0] = Nodo('break',[p[1]])
    
def p_instruccion12(p):
    'instruccion : BEGIN declaraciones END'
    p[0] = p[2]

def p_str_while(p):
    'str_while : WHILE relation DO stmts'
    p[0]= NodoWhile(p[2], p[4])

def p_str_if(p):
    'str_if : IF relation THEN stmts'
    p[0]=NodoIf(p[2],p[4])

def p_str_if_else(p):
    'str_if_else : IF relation THEN stmts ELSE stmts'
    p[0]=NodoIfElse(p[2], p[4], p[6])

def p_asign(p):
    'asign : location ASIGNACION expression'
    p[0]=NodoAsign(p[1], p[3])

def p_str_print(p):
    "str_print : PRINT '(' literal ')'"
    p[0]=Nodo('str_print',[p[3]])
    
def p_str_write(p):
    "str_write : WRITE '(' expression ')'"
    p[0]=Nodo('str_write',[p[3]])

def p_str_read(p):
    "str_read : READ '(' location ')'"
    p[0]=Nodo('str_read',[p[3]])
    
def p_str_return(p):
    'str_return : RETURN expression'
    p[0]=Nodo('str_return',[p[2]])

def p_llamada1(p):
    "llamada : IDENTIFICADOR '(' exprlist ')' "
    p[0]=Nodo('llamada',[NodoIdentificador(p[1]), p[3]])

def p_llamada2(p):
    "llamada : IDENTIFICADOR '(' ')'"
    p[0]=Nodo('llamada',[NodoIdentificador(p[1])])
    
def p_relation1(p):
    'relation : expr_or'
    p[0]= p[1]

def p_expr_or1(p):
    'expr_or : expr_and'
    p[0] = p[1]

def p_expr_or2(p):
    'expr_or : expr_or OR expr_and'
    p[0]=NodoExpr_Or(p[3], NodoOperador(p[2]), p[1])   

def p_expr_and1(p):
    'expr_and : expr_not'
    p[0] = p[1]
    
def p_expr_and2(p):
    'expr_and : expr_and AND expr_not'
    p[0]=NodoExpr_And(p[3], NodoOperador(p[2]), p[1])    

def p_expr_not1(p):
    'expr_not : comparacion'
    p[0] = p[1]
    
def p_expr_not2(p):
    'expr_not : NOT relation'
    p[0]=Nodo('expr_not',[NodoUnario(p[1], p[2])])

def p_comparacion1(p):
    'comparacion : expression oprel expression'
    p[0]= NodoComparacion(p[1], p[2],p[3])
    
def p_comparacion2(p):
    "comparacion : '(' relation ')' "
    p[0]= NodoComparacion(p[2])
    
def p_oprel1(p):
    "oprel : '<'"
    p[0]=NodoOperador(p[1])

def p_oprel2(p):
    "oprel : '>'"
    p[0]=NodoOperador(p[1])

def p_oprel3(p):
    'oprel : MENORIGUAL'
    p[0]=NodoOperador(p[1])

def p_oprel4(p):
    'oprel : MAYORIGUAL'
    p[0]=NodoOperador(p[1])
    
def p_oprel5(p):
    'oprel : IGUALIGUAL'
    p[0]=NodoOperador(p[1])
    
def p_oprel6(p):
    'oprel : DIFERENTE'
    p[0]=NodoOperador(p[1])
    
def p_exprlist1(p):
    "exprlist : exprlist ',' expression"
    p[0]= NodoExprList(p[3], p[1])
    
def p_exprlist2(p):
    'exprlist : expression'
    p[0] = NodoExprList(p[1])
      
def p_expression1(p):
    'expression : expression opsuma term'    
    p[0]=NodoExpression(p[3], p[2], p[1])
    
def p_expression2(p):
    'expression : term'    
    p[0] = p[1]


def p_opsuma1(p):
    "opsuma : '+'"
    p[0]=NodoOperador(p[1])

def p_opsuma2(p):
    "opsuma : '-'"
    p[0]=NodoOperador(p[1])

def p_term1(p):
    'term : term opmult factor'    
    p[0]= NodoTerm(p[3], p[2], p[1])
    
def p_term2(p):
    'term : factor'    
    p[0] = p[1]
    
def p_opmult1(p):
    "opmult : '*'"
    p[0]=NodoOperador(p[1])
    
def p_opmult2(p):
    "opmult : '/'"
    p[0]=NodoOperador(p[1])
    
def p_factor1(p):
    "factor : '(' expression ')'"
    p[0] = p[2]
    
def p_factor2(p):
    'factor : numero'
    p[0] = p[1]
    
def p_factor3(p):
    "factor : '-' expression %prec UMINUS"
    p[0]= NodoFactor(NodoUnario(p[1], p[2]))

def p_factor4(p):
    "factor : '+' expression %prec UPLUS"
    p[0]= NodoFactor(NodoUnario(p[1], p[2]))
    
def p_factor5(p):
    'factor : llamada'
    p[0] = p[1]
    
def p_factor6(p):
    'factor : location'
    p[0] = p[1]

def p_factor7(p):
    'factor : conversion_tipo'
    p[0] = p[1]
    
def p_location1(p):
    'location : IDENTIFICADOR'
    p[0]= NodoIdentificador(p[1])
    
def p_location2(p):
    "location : IDENTIFICADOR '[' index ']'"
    p[0]=NodoIdentificador(p[1], p[3])

def p_conversion_tipo1(p):
    "conversion_tipo : INT '(' expression ')' "
    p[0] = NodoConversionTipo(NodoTipo(p[1]), p[3])
    p[0].datatype = 'int'
    
def p_conversion_tipo2(p):
    "conversion_tipo : FLOAT '(' expression ')' "
    p[0] = NodoConversionTipo(NodoTipo(p[1]), p[3])
    p[0].datatype = 'float'
    
def p_index1(p):
    'index : expression'
    p[0] = p[1]   
    
def p_literal1(p):
    'literal : IDENTIFICADOR'
    p[0] = p[1]

def p_literal2(p):
    'literal : numero'
    p[0] = p[1]      

def p_literal3(p):
    'literal : CADENA'
    p[0] = p[1] 
    
def p_numero1(p):
    'numero : ENTERO'
    p[0]=NodoNumero(p[1])
    p[0].datatype = 'int'

def p_numero2(p):
    'numero : FLOTANTE'
    p[0]=NodoNumero(p[1])
    p[0].datatype = 'float'
    
def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Error de sintaxis cerca de '%s' en la linea %d" % (p.value,p.lineno) )
    else:
        print("Error de sintaxis al fin de linea")

import sys
import ply.yacc as yacc
yacc.yacc()

#Aumentar el limite de recursion para entradas muy grandes
sys.setrecursionlimit(5000)





def parse(data):
    try:
        root = yacc.parse(data)
        if root:
            root.accept(VisitanteTabla())
            root.accept(VisitanteTipo())
            return root
    except Exception,e:
        print e
        sys.exit()


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        f = open(filename)
        data = f.read()
        f.close()
        parse(data)
        
    except IndexError:
        while 1:
            try:
                data = raw_input('Entrada > ')
            except EOFError:
                break
            if not data: continue
            parse(data)
