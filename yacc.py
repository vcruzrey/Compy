#https://github.com/yt4766269/plytype
import json
import sys
import ply.yacc as yacc
from calc import tokens
from SymbolTable import SymbolTable
from Dato import Dato
from Tabla import Tabla
from Quadruples import Quadruples

tabla_varibles = SymbolTable()
aux_dato = Dato()
aux_tabla = Tabla()
Quadruples = Quadruples()
#comentario de prueba
#PROGRAMA
def p_programa(p):
    '''
    programa : globales funciones principal END
    '''
    p[0] = "PROGRAM COMPILED"
    #tabla_varibles = SymbolTable()

#Variables globales
#Existen: 0 o mas
def p_globales(p):
    '''
    globales : pn_crearsubdirectoriog loopglobales
    '''

def p_pn_crearsubdirectoriog(p):
    '''
    pn_crearsubdirectoriog : empty
    '''
    aux_tabla.id = 'global'
    tabla_varibles.create_table(aux_tabla.id,aux_tabla.id)

def p_loopglobales(p):
    '''
    loopglobales : declarar loopglobales
                 | empty
    '''

#Funciones
#Existen: 0 o mas
def p_funciones(p):
    '''
    funciones : funcionesloop
              | empty
    '''
    aux_tabla.reset()

def p_funcionesloop(p):
    '''
    funcionesloop : FUNC pn_st_functype ID pn_st_functionid funcparameters bloque funciones

    '''

def p_pn_st_functype(p):
    '''
    pn_st_functype : INT
                   | FLOAT
                   | BOOL
                   | STRING
                   | VOID
    '''
    aux_tabla.type = p[1]

def p_pn_st_functionid(p):
    '''
    pn_st_functionid : empty
    '''
    aux_tabla.id = p[-1]
    tabla_varibles.create_functiontable(aux_tabla)

def p_funcparameters(p):
    '''
    funcparameters : LPAREN funcparametersloop RPAREN
    '''

def p_funcparametersloop(p):
    '''
    funcparametersloop : pn_parameter tipo ID pn_currentid funcparametersloop
                       | COMMA pn_parameter tipo ID pn_currentid funcparametersloop
                       | empty
    '''

def p_pn_parameter(p):
    '''
    pn_parameter : empty
    '''
    aux_dato.parameter = True

#Principal
#Existen: 1
def p_principal(p):
    '''
    principal : MAIN pn_crearsubdirectoriom bloque
    '''
    aux_tabla.reset()

def p_pn_crearsubdirectoriom(p):
    '''
    pn_crearsubdirectoriom : empty
    '''
    aux_tabla.id = 'main'
    tabla_varibles.create_table(aux_tabla.id,aux_tabla.id)

#Bloque
def p_bloque(p):
    '''
    bloque : LCORCHO bloqueloop RCORCHO
    '''

def p_bloqueloop(p):
    '''
    bloqueloop : estatuto bloqueloop
               | asignacion bloqueloop
               | condicion bloqueloop
               | empty
    '''

#ESTATUTO
def p_estatuto(p):
    '''
    estatuto : declarar
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

#BETTER IMPLEMENTATION = PN DESPUES PNTCOMMA
def p_noinicializada(p):
    '''
    noinicializada : tipo ID pn_currentid PNTCOMMA
                   | ARR pn_currentspecial tipo ID pn_currentid bracket PNTCOMMA
                   | MAT pn_currentspecial tipo ID pn_currentid bracket bracket PNTCOMMA
    '''

def p_inicializada(p):
    '''
    inicializada : tipo ID pn_currentid copy_id pn_quadruples_addvariable inicializada_asignacion

    '''
#                 | ARR pn_currentspecial tipo ID pn_currentid bracket asignacioninicialarr
#                 | MAT pn_currentspecial tipo ID pn_currentid bracket bracket asignacioninicialmat

def p_copy_id(p):
    '''
    copy_id : empty
    '''
    p[0] = p[-2]

def p_pn_currentspecial(p):
    '''
    pn_currentspecial : empty
    '''
    if(p[-1] == 'arr'):
        aux_dato.complex = "array"
    elif(p[-1] == 'mat'):
        aux_dato.complex = "matrix"

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
    tabla_varibles.insert_variable(aux_dato, aux_tabla.id)
    aux_dato.reset()

def p_bracket(p):
    '''
    bracket : LBRCKT DTI RBRCKT
            | LBRCKT ID RBRCKT
    '''

#Asignacion
def p_asignacion(p):
    '''
    asignacion : ID pn_quadruples_addvariable EQUALS pn_quadruples_addequals expresion pn_quadruples_checkequals PNTCOMMA
    '''

def p_pn_quadruples_addequals(p):
    '''
    pn_quadruples_addequals : empty
    '''
    Quadruples.POper.append(p[-1])

def p_pn_quadruples_checkequals(p):
    '''
    pn_quadruples_checkequals : empty
    '''
    print("PN --- 11 checkequals")
    Quadruples.check_top_poper('equal')

def p_inicializada_asignacion(p):
    '''
    inicializada_asignacion : EQUALS pn_quadruples_addequals expresion pn_quadruples_checkequals PNTCOMMA
    '''

def p_asignacioninicialarr(p):
    '''
    asignacioninicialarr : EQUALS looparreglo PNTCOMMA
    '''

def p_asignacioninicialmat(p):
    '''
    asignacioninicialmat : EQUALS looparreglo looparreglo PNTCOMMA
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
    expresion : exprel pn_quadruples_checklogical expresionlogic
    '''

def p_expresionlogic(p):
    '''
    expresionlogic : AND pn_quadruples_addlogical expresion
                   | OR pn_quadruples_addlogical expresion
                   | empty
    '''

def p_pn_quadruples_checklogical(p):
    '''
    pn_quadruples_checklogical : empty
    '''
    print("PN --- 11 checklogical")
    Quadruples.check_top_poper('logical')

def p_pn_quadruples_addlogical(p):
    '''
    pn_quadruples_addlogical : empty
    '''
    print("PN --- 10 addlogical " + p[-1])
    Quadruples.POper.append(p[-1])

#Expresion Relacional
def p_exprel(p):
    '''
    exprel : exp expresionrelational pn_quadruples_checkrelational
    '''

def p_expresionrelational(p):
    '''
    expresionrelational : GREATER pn_quadruples_addrelational exp
                        | LOWER pn_quadruples_addrelational exp
                        | SAME pn_quadruples_addrelational exp
                        | LEQUAL pn_quadruples_addrelational exp
                        | GEQUAL pn_quadruples_addrelational exp
                        | NOTEQUAL pn_quadruples_addrelational exp
                        | empty
    '''

def p_pn_quadruples_checkrelational(p):
    '''
    pn_quadruples_checkrelational : empty
    '''
    print("PN --- 9 checkrelational")
    Quadruples.check_top_poper('relational')

def p_pn_quadruples_addrelational(p):
    '''
    pn_quadruples_addrelational : empty
    '''
    print("PN --- 8 addrelational " + p[-1])
    Quadruples.POper.append(p[-1])

#Exp
def p_exp(p):
    '''
    exp : termino pn_quadruples_checksumres expsumres
    '''

def p_expsumres(p):
    '''
    expsumres : PLUS pn_quadruples_addsumres exp
              | MINUS pn_quadruples_addsumres exp
              | empty
    '''

def p_pn_quadruples_checksumres(p):
    '''
    pn_quadruples_checksumres : empty
    '''
    print("PN --- 4 checksumres")
    Quadruples.check_top_poper('sumres')

def p_pn_quadruples_addsumres(p):
    '''
    pn_quadruples_addsumres : empty
    '''
    print("PN --- 8 addsumres " + p[-1])
    Quadruples.POper.append(p[-1])

#Termino
def p_termino(p):
    '''
    termino : factor pn_quadruples_checkmuldiv terminomuldiv
    '''

def p_terminomuldiv(p):
    '''
    terminomuldiv : TIMES pn_quadruples_addmuldiv termino
                  | DIVIDE pn_quadruples_addmuldiv termino
                  | empty
    '''

def p_pn_quadruples_checkmuldiv(p):
    '''
    pn_quadruples_checkmuldiv : empty
    '''
    print("PN --- 3 checkmuldiv")
    Quadruples.check_top_poper('muldiv')

def p_pn_quadruples_addmuldiv(p):
    '''
    pn_quadruples_addmuldiv : empty
    '''
    print("PN --- 2 addmuldiv " + p[-1])
    Quadruples.POper.append(p[-1])

#Factor
def p_factor(p):
    '''
    factor : LPAREN pn_quadruples_addfondo expresion RPAREN pn_quadruples_remfondo
           | vardt
    '''

def p_pn_quadruples_addfondo(p):
    '''
    pn_quadruples_addfondo : empty
    '''
    print("PN --- 6 addfondo " + p[-1])
    Quadruples.POper.append(p[-1])

def p_pn_quadruples_remfondo(p):
    '''
    pn_quadruples_remfondo : empty
    '''
    print("PN --- 7 remfondo " + p[-1])
    Quadruples.POper.pop()


#LPAREN expresion RPAREN
#       | PLUS vardt
#       | MINUS vardt

#VARDT
def p_vardt(p):
    '''
    vardt : ID pn_quadruples_addvariable
          | DTI pn_quadruples_addconstantint
          | DTF pn_quadruples_addconstantfloat
          | DTB pn_quadruples_addconstantbool
          | DTS pn_quadruples_addconstantstring
          | ID bracket
          | ID bracket bracket
    '''

def p_pn_quadruples_addvariable(p):
    '''
    pn_quadruples_addvariable : empty
    '''
    print("PN --- 1 addvariable " + p[-1])
    aux_dato.id = p[-1]
    vartest = tabla_varibles.get_variableinfo(aux_dato.id, aux_tabla.id)
    Quadruples.PilaO.append(vartest['id'])
    Quadruples.PTypes.append(vartest['type'])

def p_pn_quadruples_addconstantint(p):
    '''
    pn_quadruples_addconstantint : empty
    '''
    print("PN --- 1 addconstantint " + str(p[-1]))
    Quadruples.PilaO.append(p[-1])
    Quadruples.PTypes.append('int')

def p_pn_quadruples_addconstantfloat(p):
    '''
    pn_quadruples_addconstantfloat : empty
    '''
    print("PN --- 1 addconstantfloat " + str(p[-1]))
    Quadruples.PilaO.append(p[-1])
    Quadruples.PTypes.append('float')

def p_pn_quadruples_addconstantbool(p):
    '''
    pn_quadruples_addconstantbool : empty
    '''
    print("PN --- 1 addconstantbool " + str(p[-1]))
    Quadruples.PilaO.append(p[-1])
    Quadruples.PTypes.append('bool')

def p_pn_quadruples_addconstantstring(p):
    '''
    pn_quadruples_addconstantstring : empty
    '''
    print("PN --- 1 addconstantstring " + str(p[-1]))
    Quadruples.PilaO.append(p[-1])
    Quadruples.PTypes.append('string')

#Asignacion
def p_condicion(p):
    '''
    condicion : IF condition_if
              | WHILE condition_if
              | DO condition_if
    '''

def p_condition_if(p):
    '''
    condition_if : condition_statement pn_quadruples_addgotof bloque pn_quadruples_closegotof
    '''

def p_condition_statement(p):
    '''
    condition_statement : LPAREN expresion RPAREN
    '''

def p_pn_quadruples_addgotof(p):
    '''
    pn_quadruples_addgotof : empty
    '''
    print("PN --- CIF 1 addgotof ")
    Quadruples.addgotof()

def p_pn_quadruples_closegotof(p):
    '''
    pn_quadruples_closegotof : empty
    '''
    print("PN --- CIF 2 closegotof ")
    Quadruples.closegotof()

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print("ERROR {}".format(p))
    raise TypeError

yacc.yacc()

if __name__ == '__main__':
    try:
        arch_name = 'prueba-4.txt'
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
print("Quadruplos")
conta = 1
for q in Quadruples.PQuad:
    print(conta,q.operator,q.left_operand,q.right_operand,q.result)
    conta += 1

Quadruples.print_quad()
