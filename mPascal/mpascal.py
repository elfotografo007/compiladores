'''
Created on 27/02/2012

@author: elfotografo007
'''
#mpascal.py
import sys
import os.path
import mpasparse
import mpasgen
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
            #TODO: Modificar mpasparse.parse para retornar la raiz
            if top:
                outf = open(outname, "w")
                mpasgen.generate(outf, top)
                outf.close()
        except Exception, e:
            print e
    else:
        print 'Uso: mpasparse.py nombre_archivo_fuente'