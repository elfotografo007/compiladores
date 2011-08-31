'''
Created on 25/08/2011

@author: elfotografo007
'''
from ply import lex
#Lista de palabras reservadas del lenguaje
reserved = { 'while' : 'WHILE',
            'do' : 'DO', 
            'if' : 'IF', 
            'then' : 'THEN',
            'else' : 'ELSE',
            'fun' : 'FUN',
            'begin' : 'BEGIN',
            'end' : 'END',
            'return' : 'RETURN',
            'print' : 'PRINT',
            'write' : 'WRITE',
            'read' : 'READ',
            'skip' : 'SKIP', 
            'break' : 'BREAK', 
            'int' : 'INT', 
            'float' : 'FLOAT', 
            'and' : 'AND', 
            'or' : 'OR', 
            'not' : 'NOT'}
tokens = list(reserved.values()) + ['IDENTIFICADOR', 'ENTERO', 'FLOTANTE', 'COMENTARIO', 'CADENA', 'ASIGNACION', 'IGUALIGUAL', 'MENORIGUAL', 'MAYORIGUAL', 'DIFERENTE']

literals = ['(', ')', '[', ']', '+', '-', '*', '/', ':', ';', '<', '>', ',']

t_ignore = " \t"

def t_ignore_COMENTARIO(t):
    r"/\*(.|\n)*?\*/"
    t.lexer.lineno += t.value.count("\n")

def t_IDENTIFICADOR(t):
    r"[_a-zA-Z][_a-zA-Z\d]*"
    #Verifica que no sea una palabra reservada. Si t.value esta en reserved lo asigna, si no, lo deja como identificador
    t.type = reserved.get(t.value, 'IDENTIFICADOR') 
    return t

t_CADENA = r"\"([^\\\n]|(\\.))*\""

t_FLOTANTE = r"(\d+\.\d+)([e][+-]?\d+)?| \d+[e][+-]?\d+"

def t_ENTERO(t):
    r"\d+"
    if (t.value[0] == '0' and len(t.value) > 1):
        print "Entero ilegal: ", t.value
        t.lexer.skip(1)
    try:
        t.value = int(t.value)
    except ValueError:
        print "Entero demasiado largo", t.value
        t.value = 0
    return t

t_ASIGNACION = r":="

t_IGUALIGUAL = r"=="

t_MENORIGUAL = r"<="

t_MAYORIGUAL = r">="

t_DIFERENTE = r"!="



def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print "Error, no se identifica  ", t.value[0], "en linea ", t.lineno
    t.lexer.skip(1)

lex.lex()

if __name__ == '__main__':
    lex.runmain()