import sys
import ply.yacc as yacc
from calc import tokens
from SymbolTable import SymbolTable

vars_t = SymbolTable()

# PROGRAMA
def p_programa(p):
    '''
    programa : globales principal END
    '''
    p[0] = "PROGRAM COMPILED"

#Variables globales
#Existen: 0 o mas
def p_globales(p):
    '''
    globales : declarar globales
             | empty
    '''

def p_declarar(p):
    '''
    declarar : inicializada
             | CONS inicializada
             | noinicializada
    '''

def p_noinicializada(p):
    '''
    noinicializada : tipo ID PNTCOMMA
                   | ARR tipo ID bracket PNTCOMMA
                   | MAT tipo ID bracket bracket PNTCOMMA
    '''
    vars_t.insert_var(p[2],p[1])

#Funciones
#Existen: 0 o mas
#def p_funciones(p):
#    '''
#    funciones : metodos funciones
#              | empty
#    '''

#Principal
#Existen: 1
#def p_principal(p):
#    '''
#    principal : LCORCHO principalloop RCORCHO
#    '''

#def p_principalloop(p):
#    '''
#    principalloop : estatuto principalloop
#                  | estatuto
#                  | empty
#    '''

#ESTATUTO
#def p_estatuto(p):
#    '''
#    estatuto : declarar
#             | asignacion
#             | asignacionarr
#    '''



#def p_inicializada(p):
#    '''
#    inicializada : tipo asignacion
#                 | ARR tipo asignacioninicialarr
#                 | MAT tipo asignacioninicialmat
#    '''

def p_bracket(p):
    '''
    bracket : LBRCKT DTI RBRCKT
            | LBRCKT ID RBRCKT
    '''

# TIPO
def p_tipo(p):
    '''
    tipo : INT
         | FLOAT
         | BOOL
         | STRING
    '''
    p[0] = p[1]

# asignacion
def p_asignacion(p):
    '''
    asignacion : ID EQUALS expresion PNTCOMMA
    '''

def p_asignacionarr(p):
    '''
    asignacionarr : ID bracket EQUALS expresion PNTCOMMA
    '''

def p_asignacioninicialarr(p):
    '''
    asignacioninicialarr : ID bracket EQUALS looparreglo PNTCOMMA
    '''

def p_asignacioninicialmat(p):
    '''
    asignacioninicialmat : ID bracket bracket EQUALS looparreglo looparreglo PNTCOMMA
    '''

def p_looparreglo(p):
    '''
    looparreglo : LBRCKT expresion expresionloop RBRCKT
    '''

def p_expresionloop(p):
    '''
    expresionloop : COMMA expresion expresionloop
                  | empty
    '''

#Expresion
def p_expresion(p):
    '''
    expresion : exp expresionrelacional
    '''

def p_expresionrelacional(p):
    '''
    expresionrelacional : GREATER exp
                        | LOWER exp
                        | SAME exp
                        | LEQUAL exp
                        | GEQUAL exp
                        | NOTEQUAL exp
                        | AND exp
                        | OR exp
                        | empty
    '''

# EXP
def p_exp(p):
    '''
    exp : termino expsumres
    '''

def p_expsumres(p):
    '''
    expsumres : PLUS termino expsumres
              | MINUS termino expsumres
              | empty
    '''

#Termino
def p_termino(p):
    '''
    termino : factor terminomuldiv
    '''

def p_terminomuldiv(p):
    '''
    terminomuldiv : TIMES factor terminomuldiv
                  | DIVIDE factor terminomuldiv
                  | empty
    '''

#Factor
def p_factor(p):
    '''
    factor : LPAREN expresion RPAREN
           | PLUS vardt
           | MINUS vardt
           | vardt
    '''

#VARDT
def p_vardt(p):
    '''
    vardt : ID
          | DTI
          | DTF
          | DTB
          | DTS
          | ID bracket
          | ID bracket bracket
    '''

def p_empty(p):
    '''empty :'''

def p_error(p):
    print("ERROR {}".format(p))

yacc.yacc()

if __name__ == '__main__':
    try:
        arch_name = 'prueba-1.txt'
        arch = open(arch_name,'r')
        print("Leyendo archivo: " + arch_name + "...")
        info = arch.read()
        # print(info)
        arch.close()
        if(yacc.parse(info, tracking=True) == 'PROGRAM COMPILED'):
            print("SINTAXIS VÁLIDA")
        else:
            print("ERRORES EN LA SINTAXIS")
    except EOFError:
        print(EOFError)

print(vars_t.diccionario)

import sys
import ply.yacc as yacc
from calc import tokens
from SymbolTable import SymbolTable
from Dato import Dato

tabla_varibles = SymbolTable()
aux_dato = Dato()

# PROGRAMA
def p_programa(p):
    '''
    programa : globales END
    '''
    p[0] = "PROGRAM COMPILED"

#Variables globales
#Existen: 0 o mas
def p_globales(p):
    '''
    globales : pn_crearsubdirectorio loopglobales
             | empty
    '''

def p_pn_crearsubdirectorio(p):
    '''
    pn_crearsubdirectorio : empty
    '''
    global scope
    scope = 'global'
    name = 'global'
    tabla_varibles.create_table(name,scope)

def p_loopglobales(p):
    '''
    loopglobales : declarar loopglobales
                 | empty
    '''

def p_declarar(p):
    '''
    declarar : inicializada
             | CONS pn_currentcons inicializada
             | noinicializada
             | CONS pn_currentcons noinicializada
    '''

def p_pn_currentcons(p):
    '''
    pn_currentcons : empty
    '''
    aux_dato.cons = True

def p_noinicializada(p):
    '''
    noinicializada : tipo ID pn_currentid PNTCOMMA
                   | ARR tipo ID pn_currentid bracket PNTCOMMA
                   | MAT tipo ID pn_currentid bracket bracket PNTCOMMA
    '''

def p_inicializada(p):
    '''
    inicializada : tipo asignacion
                 | ARR tipo asignacioninicialarr
                 | MAT tipo asignacioninicialmat
    '''

# TIPO
def p_tipo(p):
    '''
    tipo : INT pn_currenttype
         | FLOAT pn_currenttype
         | BOOL pn_currenttype
         | STRING pn_currenttype
    '''

def p_pn_currenttype(p):
    '''
    pn_currenttype : empty
    '''
    aux_dato.type = p[-1]

def p_pn_currentid(p):
    '''
    pn_currentid : empty
    '''
    aux_dato.id = p[-1]
    tabla_varibles.lookup_variable(aux_dato.id, aux_dato.type, scope)
    tabla_varibles.insert_variable(aux_dato.id, aux_dato.type, scope)
    print(aux_dato.cons)
    aux_dato.reset()

    #global prueba_errortext
    #prueba_errortext = tabla_varibles.prueba_error()
    #print(prueba_errortext)


#Funciones
#Existen: 0 o mas
def p_funciones(p):
    '''
    funciones : funciones
              | empty
    '''

#Principal
#Existen: 1
def p_principal(p):
    '''
    principal : LCORCHO principalloop RCORCHO
    '''

def p_principalloop(p):
    '''
    principalloop : estatuto principalloop
                  | estatuto
                  | empty
    '''

#ESTATUTO
def p_estatuto(p):
    '''
    estatuto : declarar
             | asignacion
             | asignacionarr
    '''

def p_bracket(p):
    '''
    bracket : LBRCKT DTI RBRCKT
            | LBRCKT ID RBRCKT
    '''

# asignacion
def p_asignacion(p):
    '''
    asignacion : ID EQUALS expresion PNTCOMMA
    '''

def p_asignacionarr(p):
    '''
    asignacionarr : ID bracket EQUALS expresion PNTCOMMA
    '''

def p_asignacioninicialarr(p):
    '''
    asignacioninicialarr : ID bracket EQUALS looparreglo PNTCOMMA
    '''

def p_asignacioninicialmat(p):
    '''
    asignacioninicialmat : ID bracket bracket EQUALS looparreglo looparreglo PNTCOMMA
    '''

def p_looparreglo(p):
    '''
    looparreglo : LBRCKT expresion expresionloop RBRCKT
    '''

def p_expresionloop(p):
    '''
    expresionloop : COMMA expresion expresionloop
                  | empty
    '''

#Expresion
def p_expresion(p):
    '''
    expresion : exp expresionrelacional
    '''

def p_expresionrelacional(p):
    '''
    expresionrelacional : GREATER exp
                        | LOWER exp
                        | SAME exp
                        | LEQUAL exp
                        | GEQUAL exp
                        | NOTEQUAL exp
                        | AND exp
                        | OR exp
                        | empty
    '''

# EXP
def p_exp(p):
    '''
    exp : termino expsumres
    '''

def p_expsumres(p):
    '''
    expsumres : PLUS termino expsumres
              | MINUS termino expsumres
              | empty
    '''

#Termino
def p_termino(p):
    '''
    termino : factor terminomuldiv
    '''

def p_terminomuldiv(p):
    '''
    terminomuldiv : TIMES factor terminomuldiv
                  | DIVIDE factor terminomuldiv
                  | empty
    '''

#Factor
def p_factor(p):
    '''
    factor : LPAREN expresion RPAREN
           | PLUS vardt
           | MINUS vardt
           | vardt
    '''

#VARDT
def p_vardt(p):
    '''
    vardt : ID
          | DTI
          | DTF
          | DTB
          | DTS
          | ID bracket
          | ID bracket bracket
    '''

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print("ERROR {}".format(p))

yacc.yacc()

if __name__ == '__main__':
    try:
        arch_name = 'prueba-1.txt'
        arch = open(arch_name,'r')
        print("Leyendo archivo: " + arch_name + "...")
        info = arch.read()
        # print(info)
        arch.close()
        if(yacc.parse(info, tracking=True) == 'PROGRAM COMPILED'):
            print("SINTAXIS VÁLIDA")
        else:
            print("ERRORES EN LA SINTAXIS")
    except EOFError:
        print(EOFError)

print(tabla_varibles.diccionario)


        if (self.POper[-1] == '+' or '-'):
            right_operand = self.PilaO.Pop()
            left_operand = self.PilaO.Pop()
            right_Type = self.PTypes.Pop()
            left_Type = self.PTypes.Pop()
            operator = self.POper.Pop()
            result_Type = semantic(left_Type, right_Type, operator)
            if (result_Type == 'errorbadop'):
                raise TypeError("Unable to assign "+operator+" to types "+left_operand+", "+right_operand)
            elif (result_Type == 'errorbaddt'):
                raise TypeError("Incompatible Data Type")
            else:
                print("CreateQuad")
