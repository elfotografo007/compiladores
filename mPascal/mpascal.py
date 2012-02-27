'''
Created on 27/02/2012

@author: elfotografo007
'''
import sys
import os.path
import mpasparse
if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv
        outname = os.path.splitext(filename)[0] + ".s"
        try:
            filename = sys.argv[1]
            f = open(filename)
            data = f.read()
            f.close()
            top = mpasparse.parse(data)
        except Exception, e:
            print e
    else:
        print 'Uso: mpasparse.py nombre_archivo_fuente'