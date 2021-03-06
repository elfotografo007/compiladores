'''
Created on 25/08/2011

@author: elfotografo007
'''
#pascallex.py
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
tokens = list(reserved.values()) + ['IDENTIFICADOR',  'FLOTANTE', 'ENTERO', 'CADENA', 'ASIGNACION', 'IGUALIGUAL', 'MENORIGUAL', 'MAYORIGUAL', 'DIFERENTE']

literals = ['(', ')', '[', ']', '+', '-', '*', '/', ':', ';', '<', '>', ',']


t_ignore = " \t"

def t_ignore_COMENTARIO(t):
    r"/\*(.|\n)*?\*/"
    t.lexer.lineno += t.value.count("\n")

def t_error_comentario1(t):
    r"/\*(.|\n)*"
    print "Se ha encontrado un comentario sin cerrar : ", t.value, " en linea ", t.lineno
    t.lexer.skip(1)
    t.lexer.lineno += 1
    raise Exception('Error lexico')
    
def t_error_comentario2(t):
    r"\*/"
    print "Se ha encontrado un comentario mal formado : ", t.value, " en linea ", t.lineno
    t.lexer.skip(1)
    t.lexer.lineno += 1
    raise Exception('Error lexico')
    
#def t_error_flotante(t):
#    r".*\..*\.+.* | \d+\.\d+e(\+\++ | --+)\d+ | \d+e(\+\++ | --+)\d+ | \..* | .*e[+-]?0.* | .*\.e.*"
#    print "Se ha encontrado un flotante mal formado: ", t.value, " en linea ", t.lineno
#    t.lexer.skip(1)
#    t.lexer.lineno += 1
    
def t_FLOTANTE(t):
    r"(\d+\.\d+)([e][+-]?\d+)?| \d+[e][+-]?\d+"
    if (t.value[0] == '0' and t.value[1] != '.' and len(t.value) > 1):
        print "Flotante ilegal: ", t.value, " en linea ", t.lineno
        t.value = 0
        t.lexer.skip(1)
        t.lexer.lineno += 1
        raise Exception('Error lexico')
    #try:
     #   t.value = float(t.value)
    #except ValueError:
     #   print "Flotante demasiado largo", t.value
      #  t.value = 0
    return t

def t_error_identificador(t):
    r"\d+[_a-zA-Z]+"
    print "Se ha encontrado un Identificador mal formado: ", t.value, " en linea ", t.lineno
    t.lexer.skip(1)
    t.lexer.lineno += 1
    raise Exception('Error lexico')

def t_ENTERO(t):
    r"\d+"
    if (t.value[0] == '0' and len(t.value) > 1):
        print "Entero ilegal: ", t.value, " en linea ", t.lineno
        t.lexer.skip(1)
        t.lexer.lineno += 1
    else:
        try:
            t.value = int(t.value)
        except ValueError:
            print "Entero demasiado largo", t.value, " en linea ", t.lineno
            t.value = 0
        return t


t_ASIGNACION = r":="

t_IGUALIGUAL = r"=="

t_MENORIGUAL = r"<="

t_MAYORIGUAL = r">="

t_DIFERENTE = r"!="

def t_CADENA(t):
    r"\"([^\\\n]|(\\.))*\""
    t.value = t.value.replace(r'\"', '"')
    t.value = t.value.replace(r'\\', '\\')
    t.value = t.value.replace(r'\n', '')
    return t

def t_error_cadena(t):
    r"\".*"
    print "Cadena mal formada: ", t.value, " en linea ", t.lineno
    t.lexer.skip(1)
    t.lexer.lineno += 1
    raise Exception('Error lexico')
    
def t_IDENTIFICADOR(t):
    r"[_a-zA-Z][_a-zA-Z\d]*"
    #Verifica que no sea una palabra reservada. Si t.value esta en reserved lo asigna, si no, lo deja como identificador
    t.type = reserved.get(t.value, 'IDENTIFICADOR') 
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print "Error, no se identifica  ", t.value[0], "en linea ", t.lineno
    t.lexer.skip(1)
    raise Exception('Error lexico')

lex.lex()

if __name__ == '__main__':
    lex.runmain()