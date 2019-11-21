#https://github.com/yt4766269/plytype
import json
import sys
import ply.yacc as yacc
from calc import tokens
from SymbolTable import SymbolTable
from Memoria import Memoria
from Dato import Dato
from Dato import Parameter
from Tabla import Tabla
from Quadruples import Quadruples

tabla_varibles = SymbolTable()
aux_dato = Dato()
aux_tabla = Tabla()
aux_memoria = Memoria()
Quadruples = Quadruples()
aux_parameter = Parameter()

#comentario de prueba
#PROGRAMA
def p_programa(p):
    '''
    programa : pn_quadruples_gotomain globales funciones principal END
    '''
    p[0] = "PROGRAM COMPILED"
    #tabla_varibles = SymbolTable()

#Variables globales
#Existen: 0 o mas
def p_globales(p):
    '''
    globales : pn_crearsubdirectoriog pn_memoria_crearglobales loopglobales
    '''

def p_pn_crearsubdirectoriog(p):
    '''
    pn_crearsubdirectoriog : empty
    '''
    aux_tabla.id = 'global'
    tabla_varibles.create_table(aux_tabla.id,aux_tabla.id)

def p_pn_memoria_crearglobales(p):
    '''
    pn_memoria_crearglobales : empty
    '''
    aux_memoria.create_memoria(aux_tabla.id)
    aux_memoria.create_memoria('constantes')

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
    funcionesloop : FUNC pn_st_functype ID pn_st_functionid funcparameters bloque pn_quadruples_endproc funciones

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
    aux_memoria.create_memoria(aux_tabla.id)

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
               | empty
    '''

#ESTATUTO
def p_estatuto(p):
    '''
    estatuto : declarar
             | asignacion
             | condicion
             | ciclo
             | escritura
             | funcionvoid
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

def p_copy_id(p): #Punto neuralgico, pn
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
    aux_memoria.insert_id(aux_dato, aux_tabla.id)
    aux_dato.reset()
    #aux_dato.reset()

#def p_pn_memoria_addid(p):
#    '''
#    pn_memoria_addid : empty
#    '''
#    aux_memoria.insert_id(aux_dato, aux_tabla.id)
#    aux_dato.reset()

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
    #Print("PN --- 11 checkequals")
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
    #Print("PN --- 11 checklogical")
    Quadruples.check_top_poper('logical')

def p_pn_quadruples_addlogical(p):
    '''
    pn_quadruples_addlogical : empty
    '''
    #Print("PN --- 10 addlogical " + p[-1])
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
    #Print("PN --- 9 checkrelational")
    Quadruples.check_top_poper('relational')

def p_pn_quadruples_addrelational(p):
    '''
    pn_quadruples_addrelational : empty
    '''
    #Print("PN --- 8 addrelational " + p[-1])
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
    #Print("PN --- 4 checksumres")
    Quadruples.check_top_poper('sumres')

def p_pn_quadruples_addsumres(p):
    '''
    pn_quadruples_addsumres : empty
    '''
    #Print("PN --- 8 addsumres " + p[-1])
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
    #Print("PN --- 3 checkmuldiv")
    Quadruples.check_top_poper('muldiv')

def p_pn_quadruples_addmuldiv(p):
    '''
    pn_quadruples_addmuldiv : empty
    '''
    #Print("PN --- 2 addmuldiv " + p[-1])
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
    #Print("PN --- 6 addfondo " + p[-1])
    Quadruples.POper.append(p[-1])

def p_pn_quadruples_remfondo(p):
    '''
    pn_quadruples_remfondo : empty
    '''
    #Print("PN --- 7 remfondo " + p[-1])
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
    #Print("PN --- 1 addvariable " + p[-1])
    aux_dato.id = p[-1]
    vartest = tabla_varibles.get_variableinfo(aux_dato.id, aux_tabla.id)
    Quadruples.PilaO.append(vartest['id'])
    Quadruples.PTypes.append(vartest['type'])

def p_pn_quadruples_addconstantint(p):
    '''
    pn_quadruples_addconstantint : empty
    '''
    #Print("PN --- 1 addconstantint " + str(p[-1]))
    Quadruples.PilaO.append(p[-1])
    Quadruples.PTypes.append('int')
    aux_dato.reset()
    aux_dato.name = p[-1]
    aux_dato.type = 'int'
    aux_memoria.insert_id(aux_dato, 'constantes')
    aux_dato.reset()

def p_pn_quadruples_addconstantfloat(p):
    '''
    pn_quadruples_addconstantfloat : empty
    '''
    #Print("PN --- 1 addconstantfloat " + str(p[-1]))
    Quadruples.PilaO.append(p[-1])
    Quadruples.PTypes.append('float')
    aux_dato.reset()
    aux_dato.name = p[-1]
    aux_dato.type = 'float'
    aux_memoria.insert_id(aux_dato, 'constantes')
    aux_dato.reset()

def p_pn_quadruples_addconstantbool(p):
    '''
    pn_quadruples_addconstantbool : empty
    '''
    #Print("PN --- 1 addconstantbool " + str(p[-1]))
    Quadruples.PilaO.append(p[-1])
    Quadruples.PTypes.append('bool')
    aux_dato.reset()
    aux_dato.name = p[-1]
    aux_dato.type = 'bool'
    aux_memoria.insert_id(aux_dato, 'constantes')
    aux_dato.reset()

def p_pn_quadruples_addconstantstring(p):
    '''
    pn_quadruples_addconstantstring : empty
    '''
    #Print("PN --- 1 addconstantstring " + str(p[-1]))
    Quadruples.PilaO.append(p[-1])
    Quadruples.PTypes.append('string')
    aux_dato.reset()
    aux_dato.name = p[-1]
    aux_dato.type = 'string'
    aux_memoria.insert_id(aux_dato, 'constantes')
    aux_dato.reset()

#Condicion
def p_condicion(p):
    '''
    condicion : IF condition_statement pn_quadruples_addgotof bloque condition_else pn_quadruples_closegotodown
    '''

def p_condition_statement(p):
    '''
    condition_statement : LPAREN expresion RPAREN
    '''

def p_condition_else(p):
    '''
    condition_else : ELSE pn_quadruples_addgoto bloque
                   | empty
    '''

def p_pn_quadruples_addgotof(p):
    '''
    pn_quadruples_addgotof : empty
    '''
    #Print("PN --- CIF 1 addgotof ")
    Quadruples.addgotof()

def p_pn_quadruples_closegotodown(p):
    '''
    pn_quadruples_closegotodown : empty
    '''
    #Print("PN --- CIF 2 closegotodown ")
    Quadruples.closegotodown()

def p_pn_quadruples_addgoto(p):
    '''
    pn_quadruples_addgoto : empty
    '''
    #Print("PN --- CIF 3 addgoto ")
    Quadruples.addgoto()

#Ciclo
def p_ciclo(p):
    '''
    ciclo : WHILE ciclowhile
          | DO ciclodowhile
    '''

def p_ciclowhile(p):
    '''
    ciclowhile : pn_quadruples_addstinit condition_statement pn_quadruples_addgotof bloque pn_quadruples_addgoto pn_quadruples_closegotoup
    '''

def p_pn_quadruples_addstinit(p):
    '''
    pn_quadruples_addstinit : empty
    '''
    #Print("PN --- CWHILE 1 addstinit ")
    Quadruples.PJumps.append(len(Quadruples.PQuad) + 1)

def p_pn_quadruples_closegotoup(p):
    '''
    pn_quadruples_closegotoup : empty
    '''
    #Print("PN --- CIF 2 closegotodown ")
    Quadruples.closegotoup()

def p_ciclodowhile(p):
    '''
    ciclodowhile : pn_quadruples_addstinit bloque WHILE condition_statement pn_quadruples_addgotov PNTCOMMA
    '''

def p_pn_quadruples_addgotov(p):
    '''
    pn_quadruples_addgotov : empty
    '''
    #Print("PN --- CIF 1 addgotof ")
    Quadruples.addgotov()

#Escritura
def p_escritura(p):
    '''
    escritura : PRINT LPAREN escritura_statement escrituraloop RPAREN PNTCOMMA
    '''

def p_escrituraloop(p):
    '''
    escrituraloop : COMMA escritura_statement escrituraloop
                  | empty
    '''

def p_escritura_statement(p):
    '''
    escritura_statement : pn_quadruples_addprint expresion pn_quadruples_checkprint
    '''

def p_pn_quadruples_addprint(p):
    '''
    pn_quadruples_addprint : empty
    '''
    #Print("PN --- CIF 1 addgotof ")
    Quadruples.POper.append('print')

def p_pn_quadruples_checkprint(p):
    '''
    pn_quadruples_checkprint : empty
    '''
    #Print("PN --- CIF 1 addgotof ")
    Quadruples.check_top_poper('print')

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print("ERROR {}".format(p))
    raise TypeError

#FuncionVoid
def p_funcionvoid(p):
    '''
    funcionvoid : ID LPAREN pn_quadruples_getfuncid parameter_statement RPAREN pn_quadruples_checkfunclength PNTCOMMA
    '''

def p_parameter_statement(p):
    '''
    parameter_statement : pn_quadruples_addfuncid expresion pn_quadruples_checkfuncid parameterstatementloop
                        | empty
    '''

def p_parameterstatementloop(p):
    '''
    parameterstatementloop : COMMA pn_quadruples_addfuncid expresion pn_quadruples_checkfuncid parameterstatementloop
                           | empty
    '''

def p_pn_quadruples_getfuncid(p):
    '''
    pn_quadruples_getfuncid : empty
    '''
    #Print("PN --- 1 addvariable " + p[-1])
    funcid = p[-2]
    tabla_varibles.get_funcinfo(funcid, aux_parameter)
    Quadruples.addfuncid(funcid)

def p_pn_quadruples_addfuncid(p):
    '''
    pn_quadruples_addfuncid : empty
    '''
    #Print("PN --- CIF 1 addgotof ")
    Quadruples.addparams(aux_parameter, p.lineno(-1))

def p_pn_quadruples_checkfuncid(p):
    '''
    pn_quadruples_checkfuncid : empty
    '''
    #Print("PN --- CIF 1 addgotof ")
    Quadruples.check_top_poper('parameter')

def p_pn_quadruples_checkfunclength(p):
    '''
    pn_quadruples_checkfunclength : empty
    '''
    #Print("PN --- CIF 1 addgotof ")
    Quadruples.checkfunclenght(aux_parameter, p.lineno(-1))
    aux_parameter.reset()

def p_pn_quadruples_endproc(p):
    '''
    pn_quadruples_endproc : empty
    '''
    #Print("PN --- CIF 1 addgotof ")
    Quadruples.endproc()

def p_pn_quadruples_gotomain(p):
    '''
    pn_quadruples_gotomain : empty
    '''
    #Print("PN --- CIF 1 addgotof ")
    Quadruples.gotomain()

yacc.yacc()

if __name__ == '__main__':
    try:
        arch_name = 'memoria.txt'
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
with open('memoria.json', 'w') as outfile:
    json.dump(aux_memoria.diccionario, outfile)
print("Quadruplos")
conta = 1
for q in Quadruples.PQuad:
    print(conta,q.operator,q.left_operand,q.right_operand,q.result)
    conta += 1

Quadruples.print_quad()
