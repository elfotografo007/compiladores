'''
Created on 25/08/2011

@author: elfotografo007
'''
from ply import lex
#Lista de palabras reservadas del lenguaje
reserved = {'while' : 'WHILE', 
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
tokens = list(reserved.values()) + ['IDENTIFICADOR', 'ENTERO', 'FLOTANTE', 'COMENTARIO', 'STRING', 'ASIGNACION', 'IGUALIGUAL', 'MENORIGUAL', 'MAYORIGUAL', 'DIFERENTE']

literals = ['(', ')', '[', ']', '+', '-', '*', '/', ':', ';', '<', '>', ',' ,'\"']

t_ignore = " \t"

def t_ignore_COMENTARIO(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count("\n")

def t_IDENTIFICADOR(t):
    r"[_a-zA-Z][_a-zA-Z\d]*"
    #Verifica que no sea una palabra reservada. Si t.value esta en reserved lo asigna, si no, lo deja como identificador
    t.type = reserved.get(t.value, 'IDENTIFICADOR') 
    return t

t_ENTERO = r"0|[1-9]\d*"

t_FLOTANTE = r"(\d+\.\d+)([eE][+-]?\d+)?| \d+[eE][+-]?\d+"

t_ASIGNACION = r":="

t_IGUALIGUAL = r"=="

t_MENORIGUAL = r"<="

t_MAYORIGUAL = r">="

t_DIFERENTE = r"!="



def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print "Error, no se identifica  ", t.value, "en linea ", t.lineno
    t.lexer.skip(1)

lex.lex()

if __name__ == '__main__':
    lex.runmain()