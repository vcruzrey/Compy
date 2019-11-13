import json
import sys
import ply.yacc as yacc
from calc import tokens
from SymbolTable import SymbolTable
from Dato import Dato
from Quadruples import Quadruples

tabla_varibles = SymbolTable()
aux_dato = Dato()
Quadruples = Quadruples()

# PROGRAMA
def p_programa(p):
    '''
    programa : globales principal END
    '''
    p[0] = "PROGRAM COMPILED"
    #tabla_varibles = SymbolTable()

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

#Declaracion
def p_declarar(p):
    '''
    declarar : noinicializada
             | inicializada
             | CONS pn_currentcons inicializada
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
    inicializada : tipo ID pn_currentid inicializada_asignacion
                 | ARR tipo asignacioninicialarr
                 | MAT tipo asignacioninicialmat
    '''

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
    tabla_varibles.insert_variable(aux_dato, scope)
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
    principal : MAIN LCORCHO principalloop RCORCHO
    '''

def p_principalloop(p):
    '''
    principalloop : asignacion principalloop
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

def p_inicializada_asignacion(p):
    '''
    inicializada_asignacion : EQUALS expresion PNTCOMMA
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
    exp : termino pn_quadruples_checksum expsumres
    '''

def p_expsumres(p):
    '''
    expsumres : PLUS pn_quadruples_sum termino pn_quadruples_checksum expsumres
              | MINUS pn_quadruples_sum termino pn_quadruples_checksum expsumres
              | empty
    '''

#Termino
def p_termino(p):
    '''
    termino : factor terminomuldiv
    '''

def p_terminomuldiv(p):
    '''
    terminomuldiv : TIMES pn_quadruples_mult factor terminomuldiv
                  | DIVIDE pn_quadruples_mult factor terminomuldiv
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
    vardt : ID pn_quadruples_getvariable
          | DTI
          | DTF
          | DTB
          | DTS
          | ID bracket
          | ID bracket bracket
    '''

#VARDT
def p_pn_quadruples_getvariable(p):
    '''
    pn_quadruples_getvariable : empty
    '''
    Quadruples.PilaO.append(p[-1])
    Quadruples.PTypes.append('int')

#VARDT
def p_pn_quadruples_sum(p):
    '''
    pn_quadruples_sum : empty
    '''
    Quadruples.POper.append(p[-1])

def p_pn_quadruples_mult(p):
    '''
    pn_quadruples_mult : empty
    '''
    Quadruples.POper.append(p[-1])

def p_pn_quadruples_checksum(p):
    '''
    pn_quadruples_checksum : empty
    '''
    Quadruples.checksum()

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print("ERROR {}".format(p))



#Cambios Rolando

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

with open('data.json', 'w') as outfile:
    json.dump(tabla_varibles.diccionario, outfile)

Quadruples.print_quad()
