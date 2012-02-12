'''
Created on 10/02/2012

@author: elfotografo007
'''
#symtab.py
class symtab(object):
    '''
    Clase Tabla de Simbolos
    '''
    
    def __init__(self):
        self.__ambitos = [{}]
        self.__current = self.__ambitos[0]
        
    def popAmbito(self):
        ambito = self.__ambitos.pop()
        self.__current = self.__ambitos[-1]
        return ambito
    
    def pushAmbito(self):
        self.__ambitos.append({})
        self.__current = self.__ambitos[-1]
        return self.__current
   
    def existe(self, simbolo):
        for i in self.__ambitos:
            if  simbolo in i:
                return True, i
        return False, None
    
    def agregar(self, llave):
        self.__current[llave] = {}
    
    def setAtributo(self, simbolo, llave, valor):
        self.__current[simbolo][llave] = valor
    
    def getCurrent(self):
        return self.__current
        
    
    
    
    
    