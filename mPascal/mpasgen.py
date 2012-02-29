'''
Created on 27/02/2012

@author: elfotografo007
'''
#mpasgen.py

from StringIO import StringIO
from Visitante import Visitante
from Nodo import Nodo, NodoEstructuraFuncion, NodoArguments, NodoArg, NodoLocals,\
    NodoDeclaraciones, NodoWhile, NodoIf, NodoIfElse, NodoAsign,\
    NodoIdentificador, NodoExprList, NodoExpression, NodoTerm, NodoFactor,\
    NodoUnario, NodoExpr_And, NodoExpr_Or, NodoComparacion,NodoStmts,NodoIndex,NodoRelation,\
    NodoNumero
    

    
class VisitanteGenerar(Visitante):
    
    def __init__(self, file):
        self.file = file
        self.argCount = 1
        self.data = StringIO()
        self.labelCount = 0
        self.regCount = 0
        self.regList = {}
        self.endLabel = None
        
    def new_label(self):
        self.labelCount += 1
        return ".L%d" % self.labelCount
    
    def push(self):
        registro = "$s%d" % self.regCount
        if self.regCount > 7:
            registro = "$s%d" % (self.regCount-8)
            if registro not in self.regList:
                print >>self.file, "    addi $sp,$sp, -4"
                print >>self.file, "    sw %s, 0($sp)" % registro
            self.regList[registro] = False
        self.regCount += 1
        return registro
    
    def pop(self):
        self.regCount -= 1
        registro = "$s%d" % self.regCount
        if self.regCount > 7:
            registro = "$s%d" % (self.regCount-8)
        if len(self.regList) > 0:
            if registro in self.regList:
                if self.regList[registro]:
                    print >>self.file, "    lw %s, 0($sp)" % registro
                    print >>self.file, "    addi $sp,$sp, 4"
                    del self.regList[registro]
                else:
                    self.regList[registro] = True
        return registro
    
    def generate(self, top):
        print >>self.file, "!Creado por mpascal.py"
        print >>self.file, "! Esteban Santa y Andres Torres, IS744 (2012-1)"
        print >>self.file, '    .section ".text"'
        print >>self.data, '    .section ".data"'
        self.visiteme(top)
        print >>self.file, self.data.getvalue()
        
    def visiteme(self, objeto):
        if isinstance(objeto, Nodo):
            if objeto.etiqueta == 'programa':
                print >>self.file, "\n! programa"
                for hoja in objeto.hojas:
                    hoja.accept(self)
                    
            if objeto.etiqueta == 'str_write':
                print >>self.file, "\n! write (start)"
                for hoja in objeto.hojas:
                    hoja.accept(self)
                print >>self.file, "!  expr := pop"
                print >>self.file, "!  write(expr)"
                if objeto.hojas[0].datatype == 'int':
                    print >>self.file, "!  call mwritei(int)"
                    print >>self.file, "    move expr, $v0"#TODO: verificar que se hace aqui con el expr
                    print >>self.file, "    call mwritei"
                    print >>self.file, "    nop" 
                elif objeto.hojas[0].datatype == 'float':
                    print >>self.file, "!  call mwritef(float)"
                    print >>self.file, "    move expr, $v0"#TODO: verificar que se hace aqui con el expr
                    print >>self.file, "    call mwritef"
                    print >>self.file, "    nop" 
                print >>self.file, "! write (end)"
                
            if objeto.etiqueta == 'declaraciones_funcion':
                for hoja in objeto.hojas:
                    hoja.accept(self)
                    
            if objeto.etiqueta == 'str_read':
                print >>self.file, "\n! read (start)"
                if objeto.hojas[0].datatype == 'int':
                    print >>self.file, "!  call mreadi()"
                    print >>self.file, "    call mreadi"
                    print >>self.file, "    nop" 
                    print >>self.file, "    sw $v0, result"#TODO: donde se guarda lo que ha sido leido?
                elif objeto.hojas[0].datatype == 'float':
                    print >>self.file, "!  call mreadf()"
                    print >>self.file, "    call mreadf"
                    print >>self.file, "    nop" 
                    print >>self.file, "    sw $v0, result"#TODO: donde se guarda lo que ha sido leido?
                print >>self.file, "! read (end)"
            
            if objeto.etiqueta == 'str_print':
                print >>self.file, "\n! print (start)"
                label = self.new_label()
                print >>self.data, '{0}:  .asciiz {1}'.format(label, objeto.hojas[0])
                print >>self.file, '    lui $v0, ', label
                print >>self.file, '    ori $v0, $v0, ', label
                print >>self.file, '    call mprint'
                print >>self.file, "! print (end)"
            
            if objeto.etiqueta == 'expr_not':
                for hoja in objeto.hojas:
                    hoja.accept(self)
                    
            if objeto.etiqueta == 'llamada':
                if len(objeto.hojas) > 1:
                    self.argCount = 1
                    objeto.hojas[1].accept(self)
                    if not isinstance(objeto.hojas[1], NodoExprList):
                        print >>self.file, "arg1 := pop"
                    args = ''
                    for i in range(1,self.argCount):
                        args += 'arg%d,' % i
                    print >>self.file, "!  push {0}({1})".format(objeto.hojas[0].identificador, args.rstrip(','))
                else:
                    print >>self.file, "! push %s()" % objeto.hojas[0].identificador

            if objeto.etiqueta == 'str_return':
                print >>self.file, "\n! return (start)"
#                for hoja in objeto.hojas:
#                    hoja.accept(self)
                print >>self.file, "! return (end)"
        
        elif isinstance(objeto, NodoEstructuraFuncion):
                id = objeto.identificador.identificador
                variables = objeto.locales
                print >>self.file, "\n! funcion %s (start)" % id
                print >>self.file, "    .global ", id
                print >>self.file, "%s:" % id
                elementos = 0
                if len(variables) > 0:
                    for variable in variables:
                        if variables[variable]['tipo'] == 'variable':
                            elementos += 4
                            variables[variable]['offset'] = elementos * -1
                        else:
                            elementos += 4*variables[variable]['size']
                            variables[variable]['offset'] = elementos * -1
                    print >>self.file, "    addi $sp, $sp, -", elementos + 64
                if objeto.locals:
                    objeto.locals.accept(self)
                objeto.declaraciones.accept(self)
                print>>self.file, self.new_label()
                
                if len(variables) > 0:
                    print >>self.file, "    addi $sp, $sp, ", elementos
                
                if id == 'main':
                    print >>self.file, "    add $v0, $zero,$zero"
                    print >>self.file, "    call _exit"
                    print >>self.file, "    nop"
                else:
                    print >>self.file, "    jr $ra"#TODO: Verificar si jr $ra tambien se incluye en main o no
                
                print >>self.file, "! funcion %s (end)" % id
        
        elif isinstance(objeto, NodoArguments):
            if objeto.arguments:
                objeto.arguments.accept(self)
            objeto.arg.accept(self)
            
        elif isinstance(objeto, NodoArg):
            pass
        
        elif isinstance(objeto, NodoLocals):
            if objeto.locals:
                objeto.locals.accept(self)
            objeto.arg.accept(self)
            
        elif isinstance(objeto, NodoDeclaraciones) or isinstance(objeto, NodoStmts):
            if objeto.declaraciones:
                objeto.declaraciones.accept(self)
            objeto.instruccion.accept(self)
            
        elif isinstance(objeto, NodoWhile):
            print >>self.file, "\n! while (start)"
            loop_label = self.new_label()
            end_loop_label = self.new_label()
            print >>self.file, "%s:"  % loop_label
            objeto.relation.accept(self)
            print >>self.file, "    beq {0}, $zero, {1}".format(self.pop(), end_loop_label)
            print >>self.file, "    nop"
            objeto.stmts.accept(self)
            print >>self.file, "    j ", loop_label
            print >>self.file, "%s:" % end_loop_label
            print >>self.file, "! while (end)"
            del loop_label
            del end_loop_label
            
        elif isinstance(objeto, NodoIf):
            print >>self.file, "\n! if (start)"
            objeto.relation.accept(self)
            end_if_label = self.new_label()
            print >>self.file, "    beq {0}, $zero, {1}".format(self.pop(), end_if_label)
            print >>self.file, "    nop"
            objeto.stmts.accept(self)
            print >>self.file, "%s:" % end_if_label
            print >>self.file, "! if (end)"
            del end_if_label
            
        elif isinstance(objeto, NodoIfElse):
            print >>self.file, "\n! if (start)"
            end_if_label = self.new_label()
            else_label = self.new_label()
            objeto.relation.accept(self)
            print >>self.file, "    beq {0}, $zero, {1}".format(self.pop(), end_if_label)
            print >>self.file, "    nop"
            objeto.stmts1.accept(self)
            print >>self.file, "    j ", end_if_label
            print >>self.file, "%s:" % else_label
            objeto.stmts2.accept(self)
            print >>self.file, "%s:" % end_if_label
            print >>self.file, "! if (end)"
            del end_if_label
            del else_label
            
        elif isinstance(objeto, NodoAsign):
            print >>self.file, "\n! assign (start)"
            objeto.expression.accept(self)
            print >>self.file, "!  %s := pop" % objeto.location.identificador
            print >>self.file, "! assign (end)"
            
        elif isinstance(objeto, NodoIdentificador):
            id = objeto.identificador
            if objeto.index:
                objeto.index.accept(self)
                print >>self.file, "!  index := pop"
                print >>self.file, "!  push %s[index]" % id
                print >>self.file, "    lw {0}, {1}($fp)".format(self.push(), str(objeto.ambito[id]['offset'] + (objeto.index.expression*4)))
            else:
                print >>self.file, "!  push", id
                print >>self.file, "    lw {0}, {1}($fp)".format(self.push(), str(objeto.ambito[id]['offset']))
                
        
        elif isinstance(objeto, NodoExprList):
            if objeto.exprlist:
                objeto.exprlist.accept(self)
            objeto.expression.accept(self)
            print >>self.file, "!  arg%d := pop" % self.argCount
            self.argCount += 1
            
        elif isinstance(objeto, NodoExpression):
            if objeto.expression:
                objeto.expression.accept(self)               
            objeto.term.accept(self)
            rs = self.pop()
            rt = self.pop()
            if objeto.op.op == '+':
                print >>self.file, "!  add"
                print >>self.file, "    add {0}, {1},{2}".format(self.push(), rs, rt)
            else:
                print >>self.file, "!  sub"
                print >>self.file, "    sub {0}, {1},{2}".format(self.push(), rs, rt)
            
        elif isinstance(objeto, NodoTerm):
            if objeto.term:
                objeto.term.accept(self)
            objeto.factor.accept(self)          
            if objeto.op.op == '*':
                print >>self.file, "!  mul"
            else:
                print >>self.file, "!  div"
            
        elif isinstance(objeto, NodoFactor):
            objeto.expression.accept(self)
            
        elif isinstance(objeto, NodoUnario):
            objeto.expression.accept(self)

        elif isinstance(objeto, NodoExpr_Or):
            if objeto.expr_or:
                objeto.expr_or.accept(self)
            objeto.expr_and.accept(self)
            print >> self.file, "!  or"
            rs = self.pop()
            rt = self.pop()
            print >>self.file, "    or {0}, {1},{2}".format(self.push(), rs, rt)
            
        elif isinstance(objeto, NodoExpr_And):
            if objeto.expr_and:
                objeto.expr_and.accept(self)
            objeto.expr_not.accept(self)
            print >> self.file, "!  and"
            rs = self.pop()
            rt = self.pop()
            print >>self.file, "    and {0}, {1},{2}".format(self.push(), rs, rt)
            
        elif isinstance(objeto, NodoComparacion):
            objeto.expression1.accept(self)
            if objeto.expression2:
                objeto.expression2.accept(self)
                if objeto.op.op == '<':
                    print >>self.file, "!  lt"
                    rt = self.pop()
                    rs = self.pop()
                    print >>self.file, "    slt {0}, {1}, {2}".format(self.push(), rs,rt)
                elif objeto.op.op == '>':
                    print >>self.file, "!  gt"
                    rt = self.pop()
                    rs = self.pop()
                    print >>self.file, "    slt {0}, {1}, {2}".format(self.push(), rt,rs)
                elif objeto.op.op == '<=':
                    print >>self.file, "!  lte"
                    rt = self.pop()
                    rs = self.pop()
                    print >>self.file, "    slt $t0, {1}, {2}".format(rt,rs)
                    print >>self.file, "    nor %s, $t0, $zero"  % self.push()
                elif objeto.op.op == '>=':
                    print >>self.file, "!  gte"
                    rt = self.pop()
                    rs = self.pop()
                    label = self.new_label()
                    print >>self.file, "    slt $t0, {1}, {2}".format(rs,rt)
                    print >>self.file, "    nor %s, $t0, $zero"  % self.push()
                elif objeto.op.op == '==':
                    print >>self.file, "!  eq"
                    rt = self.pop()
                    rs = self.pop()
                    print >>self.file, "    slt $t0, {1}, {2}".format(rs,rt)
                    print >>self.file, "    slt $t1, {1}, {2}".format(rt,rs)
                    print >>self.ifle, "    and %s,$t0,$t1" % self.push()
                elif objeto.op.op == '!=':
                    print >>self.file, "!  ne"
                    rt = self.pop()
                    rs = self.pop()
                    print >>self.file, "    slt $t0, {1}, {2}".format(rs,rt)
                    print >>self.file, "    slt $t1, {1}, {2}".format(rt,rs)
                    print >>self.file, "    and $t2,$t0,$t1"
                    print >>self.file, "    nor %s, $t2, $zero"  % self.push()
                
        elif isinstance(objeto, NodoNumero):
            numero = objeto.expression
            print >>self.file, "!  push", numero
            if abs(numero) <= 4095:
                print >>self.file, "    move {0}, {1}".format(self.push(),str(numero))
            else:
                label = self.new_label()
                print >>self.file, '    la $t0, ', label#TODO: Verificar que asi se hace la parte de las etiquetas 
                print >>self.file, '    lw %s, 0($t0)' % self.push()
                if objeto.datatype == 'int': 
                    print >>self.data, '{0}:  .word  {1}'.format(label, str(numero))
                else:
                    print >>self.data, '{0}:  .float  {1}'.format(label, str(numero))
                