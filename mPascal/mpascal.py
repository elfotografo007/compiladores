'''
Created on 27/02/2012

@author: elfotografo007
'''
#mpascal.py
import sys
import os.path
import mpasparse
from mpasgen import VisitanteGenerar
if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        outname = os.path.splitext(filename)[0] + ".s"
        try:
            filename = sys.argv[1]
            f = open(filename)
            data = f.read()
            f.close()
            top = mpasparse.parse(data)
            if top:
                outf = open(outname, "w")
                visitante = VisitanteGenerar(outf)
                visitante.generate(top)
                outf.close()
        except Exception, e:
            print e
#        filename = sys.argv[1]
#        f = open(filename)
#        data = f.read()
#        f.close()
#        top = mpasparse.parse(data)
#        if top:
#            outf = open(outname, "w")
#            visitante = VisitanteGenerar(outf)
#            visitante.generate(top)
#            outf.close()

    else:
        print 'Uso: mpasparse.py nombre_archivo_fuente'