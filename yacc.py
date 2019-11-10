import sys
import ply.yacc as yacc
from calc import tokens
from SymbolTable import SymbolTable

tabla_varibles = SymbolTable()
type = None
scope = None
name = None
id = None

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
             | CONS inicializada
             | noinicializada
    '''

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
    type = p[-1]

def p_pn_currentid(p):
    '''
    pn_currentid : empty
    '''
    id = p[-1]
    tabla_varibles.insert_variable(id, type, scope)
    global prueba_errortext
    prueba_errortext = tabla_varibles.prueba_error()
    print(prueba_errortext)

#Funciones
#Existen: 0 o mas
#def p_funciones(p):
#    '''
#    funciones : metodos funciones
#              | empty
#    '''

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
