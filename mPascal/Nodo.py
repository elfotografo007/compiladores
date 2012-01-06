'''
Created on 06/01/2012

@author: elfotografo007
'''
class Nodo(object):
    def __init__(self, etiqueta = ' ', hojas = []):
        self.hojas = hojas
        self.etiqueta = etiqueta
    def agregarHoja(self, objeto):
        self.hojas.append(objeto)
    
    def imprimir(self, nivel):
        print self.etiqueta
        for i in self.hojas:
            print '|__' * nivel,
            if isinstance(i, Nodo):
                i.imprimir(nivel + 1)
            else:
                print i