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
Quadruples = Quadruples()
aux_parameter = Parameter()
#comentario de prueba
#PROGRAMA
def p_programa(p):
    '''
    programa : globales pn_quadruples_gotomain funciones principal muere
    '''
    p[0] = "PROGRAM COMPILED"

#Variables globales
#Existen: 0 o mas
def p_globales(p):
    '''
    globales : pn_st_createtableglocons loopglobales
    '''

def p_pn_st_createtableglocons(p):
    '''
    pn_st_createtableglocons : empty
    '''
    aux_tabla.name = 'global'
    aux_tabla.type = 'global'
    tabla_varibles.create_table_globalcons('global')
    tabla_varibles.create_table_globalcons('constantes')

def p_loopglobales(p):
    '''
    loopglobales : declarar loopglobales
                 | empty
    '''

#Funciones
#Existen: 0 o mas
def p_funciones(p):
    '''
    funciones : pn_quadruples_resettemporales funcionesloop
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
    aux_tabla.name = p[-1]
    aux_tabla.posicion_inical = Quadruples.get_position()
    tabla_varibles.create_table_function(aux_tabla, p.lineno(-1))

def p_funcparameters(p):
    '''
    funcparameters : LPAREN funcparametersloop RPAREN
    '''

def p_funcparametersloop(p):
    '''
    funcparametersloop : pn_parameter tipo ID pn_st_insertvariable funcparametersloop
                       | pn_parameter ARR pn_dato_currentspecialsn tipo ID pn_st_insertvariable funcparametersloop
                       | COMMA pn_parameter tipo ID pn_st_insertvariable funcparametersloop
                       | COMMA pn_parameter ARR pn_dato_currentspecialsn tipo ID pn_st_insertvariable funcparametersloop
                       | empty
    '''

def p_pn_parameter(p):
    '''
    pn_parameter : empty
    '''
    aux_dato.parameter = True
    aux_dato.cons = False
    aux_dato.complex = "simple"

#Principal
#Existen: 1
def p_principal(p):
    '''
    principal : MAIN pn_st_createtablemain pn_quadruples_checkgotomain pn_quadruples_resettemporales bloque
    '''
    aux_tabla.reset()

def p_pn_st_createtablemain(p):
    '''
    pn_st_createtablemain : empty
    '''
    aux_tabla.name = "main"
    aux_tabla.type = "main"
    tabla_varibles.create_table_main()

def p_pn_quadruples_checkgotomain(p):
    '''
    pn_quadruples_checkgotomain : empty
    '''
    #print("PN Quadruples --- 12 checkequals")
    Quadruples.check_gotomain()

def p_pn_quadruples_resettemporales(p):
    '''
    pn_quadruples_resettemporales : empty
    '''
    #print("PN Quadruples --- 12 checkequals")
    Quadruples.reset_temporales()

#Bloque
def p_bloque(p):
    '''
    bloque : LCORCHO bloqueloop RCORCHO
    '''

def p_bloquefunc(p):
    '''
    bloquefunc : LCORCHO bloqueloop RCORCHO
    '''

def p_return_statement(p):
    '''
    return_statement : RETURN condition_statement pn_quadruples_checkreturn PNTCOMMA
    '''

def p_pn_quadruples_checkreturn(p):
    '''
    pn_quadruples_checkreturn : empty
    '''
    vardato = tabla_varibles.get_variable(aux_tabla.name, 'return', p.lineno(-1))
    Quadruples.PilaDato.append(vardato)
    Quadruples.POper.append('return')
    Quadruples.check_top_poper('return', p.lineno(-1))

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
             | asignacionarr
             | asignacionarrvar
             | condicion
             | ciclo
             | escritura
             | funcionvoid
             | return_statement
    '''

#Declarar
def p_declarar(p):
    '''
    declarar : noinicializada
             | inicializada
             | CONS pn_dato_currentcons inicializada
    '''

def p_noinicializada(p):
    '''
    noinicializada : tipo ID pn_st_insertvariable PNTCOMMA
                   | ARR pn_dato_currentspecial tipo ID bracket copy_id pn_st_insertvariable PNTCOMMA
                   | MAT pn_dato_currentspecial tipo ID bracket copy_id bracket copy_id pn_st_insertvariable PNTCOMMA
    '''

def p_inicializada(p):
    '''
    inicializada : tipo ID pn_st_insertvariable copy_id pn_quadruples_addvariable inicializada_asignacion

    '''

def p_pn_dato_currentcons(p):
    '''
    pn_dato_currentcons : empty
    '''
    aux_dato.cons = True

def p_copy_id(p):
    '''
    copy_id : empty
    '''
    p[0] = p[-2]

def p_pn_dato_currentspecial(p):
    '''
    pn_dato_currentspecial : empty
    '''
    aux_dato.complex = p[-1]

def p_pn_dato_currentspecialsn(p):
    '''
    pn_dato_currentspecialsn : empty
    '''
    aux_dato.complex = p[-1] + "sn"

def p_bracket(p):
    '''
    bracket : LBRCKT DTI pn_dato_currenttamano RBRCKT
    '''

def p_pn_dato_currenttamano(p):
    '''
    pn_dato_currenttamano : empty
    '''
    aux_dato.tamano.append(p[-1])

def p_tipo(p):
    '''
    tipo : INT pn_dato_currenttype
         | FLOAT pn_dato_currenttype
         | BOOL pn_dato_currenttype
         | STRING pn_dato_currenttype
    '''

def p_pn_dato_currenttype(p):
    '''
    pn_dato_currenttype : empty
    '''
    aux_dato.type = p[-1]

def p_pn_st_insertvariable(p):
    '''
    pn_st_insertvariable : empty
    '''
    aux_dato.name = p[-1]
    tabla_varibles.insert_variable(aux_dato, aux_tabla, p.lineno(-1))
    aux_dato.reset()

#Asignacion
def p_asignacion(p):
    '''
    asignacion : ID pn_quadruples_addvariable EQUALS pn_quadruples_addequals expresion pn_quadruples_checkequals PNTCOMMA
    '''

def p_asignacionarr(p):
    '''
    asignacionarr : ID LBRCKT DTI RBRCKT pn_quadruples_addvariablearr EQUALS pn_quadruples_addequals expresion pn_quadruples_checkequals PNTCOMMA
    '''
def p_asignacionarrvar(p):
    '''
    asignacionarrvar : ID LBRCKT ID RBRCKT pn_quadruples_addvariablearrvar EQUALS pn_quadruples_addequals expresion pn_quadruples_checkequals PNTCOMMA
    '''

def p_inicializada_asignacion(p):
    '''
    inicializada_asignacion : EQUALS pn_quadruples_addequals expresion pn_quadruples_checkequals PNTCOMMA
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
    #print("PN Quadruples --- 12 checkequals")
    Quadruples.check_top_poper('equal', p.lineno(-1))

#Expresion
def p_expresion(p):
    '''
    expresion : exprel pn_quadruples_checklogical expresionlogical
    '''

def p_expresionlogical(p):
    '''
    expresionlogical : AND pn_quadruples_addlogical expresion
                     | OR pn_quadruples_addlogical expresion
                     | empty
    '''

def p_pn_quadruples_checklogical(p):
    '''
    pn_quadruples_checklogical : empty
    '''
    #Print("PN Quadruples --- 11 checklogical")
    Quadruples.check_top_poper('logical', p.lineno(-1))

def p_pn_quadruples_addlogical(p):
    '''
    pn_quadruples_addlogical : empty
    '''
    #Print("PN Quadruples --- 10 addlogical " + p[-1])
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
    #Print("PN Quadruples --- 9 checkrelational")
    Quadruples.check_top_poper('relational', p.lineno(-1))

def p_pn_quadruples_addrelational(p):
    '''
    pn_quadruples_addrelational : empty
    '''
    #Print("PN Quadruples --- 8 addrelational " + p[-1])
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
    #Print("PN Quadruples--- 4 checksumres")
    Quadruples.check_top_poper('sumres', p.lineno(-1))

def p_pn_quadruples_addsumres(p):
    '''
    pn_quadruples_addsumres : empty
    '''
    #Print("PN Quadruples --- 8 addsumres " + p[-1])
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
    #Print("PN Quadruples --- 3 checkmuldiv")
    Quadruples.check_top_poper('muldiv', p.lineno(-1))

def p_pn_quadruples_addmuldiv(p):
    '''
    pn_quadruples_addmuldiv : empty
    '''
    #Print("PN Quadruples --- 2 addmuldiv " + p[-1])
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
    #print("PN Quadruples --- 6 addfondo " + p[-1])
    Quadruples.POper.append(p[-1])

def p_pn_quadruples_remfondo(p):
    '''
    pn_quadruples_remfondo : empty
    '''
    #print("PN Quadruples --- 7 remfondo " + p[-1])
    Quadruples.POper.pop()

#VARDT
def p_vardt(p):
    '''
    vardt : ID pn_quadruples_addvariable
          | DTI pn_quadruples_addconstantint
          | DTF pn_quadruples_addconstantfloat
          | TRUE pn_quadruples_addconstantbool
          | FALSE pn_quadruples_addconstantbool
          | DTS pn_quadruples_addconstantstring
          | ID LBRCKT DTI RBRCKT pn_quadruples_addvariablearr
          | ID LBRCKT ID RBRCKT pn_quadruples_addvariablearrvar
          | funcionvoid_vardt pn_quadruples_addfuncion
          | LEN LPAREN ID RPAREN pn_quadruples_getarrlen
          | STR LPAREN ID RPAREN pn_quadruples_insert_str
    '''

def p_pn_quadruples_addvariable(p):
    '''
    pn_quadruples_addvariable : empty
    '''
    #print("PN --- 1 addvariable " + p[-1])
    aux_dato.name = p[-1]
    vardato = tabla_varibles.get_variable(aux_dato.name, aux_tabla.name, p.lineno(-1))
    Quadruples.PilaDato.append(vardato)

def p_pn_quadruples_addfuncion(p):
    '''
    pn_quadruples_addfuncion : empty
    '''
    #print("PN --- 1 addvariable " + p[-1])
    vardato = tabla_varibles.get_variable(aux_dato.name, 'global', p.lineno(-1))
    Quadruples.create_return_temporal(vardato)

def p_pn_quadruples_addvariablearr(p):
    '''
    pn_quadruples_addvariablearr : empty
    '''
    #print("PN --- 1 addvariablearr " + p[-1])
    aux_dato.name = p[-4]
    index = p[-2]
    vardato = tabla_varibles.get_variable(aux_dato.name, aux_tabla.name, p.lineno(-1))
    print(vardato)
    Quadruples.get_variable_arr(vardato, index, p.lineno(-1))

def p_pn_quadruples_addvariablearrvar(p):
    '''
    pn_quadruples_addvariablearrvar : empty
    '''
    #print("PN --- 1 addvariablearr " + p[-1])
    aux_dato.name = p[-4]
    index = tabla_varibles.get_variable(p[-2], aux_tabla.name, p.lineno(-1))
    vardato = tabla_varibles.get_variable(aux_dato.name, aux_tabla.name, p.lineno(-1))
    direccion = "("+str(index['direccion'])+")"
    Quadruples.get_variable_arr(vardato, direccion, p.lineno(-1))
    #Quadruples.PilaO.append(vartest['name'])
    #Quadruples.PTypes.append(vartest['type'])

def p_pn_quadruples_addconstantint(p):
    '''
    pn_quadruples_addconstantint : empty
    '''
    #print("PN --- 1 addconstantint " + str(p[-1]))
    vardato = tabla_varibles.get_constant(p[-1], 'int', p.lineno(-1))
    Quadruples.PilaDato.append(vardato)

def p_pn_quadruples_addconstantfloat(p):
    '''
    pn_quadruples_addconstantfloat : empty
    '''
    #print("PN --- 1 addconstantfloat " + str(p[-1]))
    vardato = tabla_varibles.get_constant(p[-1], 'float', p.lineno(-1))
    Quadruples.PilaDato.append(vardato)

def p_pn_quadruples_addconstantbool(p):
    '''
    pn_quadruples_addconstantbool : empty
    '''
    #print("PN --- 1 addconstantbool " + str(p[-1]))
    vardato = tabla_varibles.get_constant(p[-1], 'bool', p.lineno(-1))
    Quadruples.PilaDato.append(vardato)

def p_pn_quadruples_addconstantstring(p):
    '''
    pn_quadruples_addconstantstring : empty
    '''
    #print("PN --- 1 addconstantstring " + str(p[-1]))
    vardato = tabla_varibles.get_constant(p[-1], 'string', p.lineno(-1))
    Quadruples.PilaDato.append(vardato)

def p_pn_quadruples_getarrlen(p):
    '''
    pn_quadruples_getarrlen : empty
    '''
    #print("PN --- 1 addconstantstring " + str(p[-1]))
    aux_dato.name = p[-2]
    vardato = tabla_varibles.get_variable(aux_dato.name, aux_tabla.name, p.lineno(-1))
    Quadruples.get_variable_arr_len(vardato, p.lineno(-1))

def p_pn_quadruples_insert_str(p):
    '''
    pn_quadruples_insert_str : empty
    '''
    #print("PN --- 1 addconstantstring " + str(p[-1]))
    aux_dato.name = p[-2]
    vardato = tabla_varibles.get_variable(aux_dato.name, aux_tabla.name, p.lineno(-1))
    Quadruples.pn_quadruples_insert_str(vardato)


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
    Quadruples.check_top_poper('print', p.lineno(-1))

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

def p_funcionvoid_vardt(p):
    '''
    funcionvoid_vardt : ID LPAREN pn_quadruples_getfuncid parameter_statement RPAREN pn_quadruples_checkfunclength
    '''
    aux_dato.name = p[1]

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
    tabla_varibles.get_function_info(funcid, aux_parameter, p.lineno(-1))
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
    right_operand = Quadruples.PilaDato.pop()
    left_operand = Quadruples.PilaDato.pop()
    tabla_varibles.check_param_arr(right_operand,left_operand,aux_parameter.name, p.lineno(-1))
    inicio = tabla_varibles.diccionario['dirFunc'][aux_parameter.name]['inicio']
    Quadruples.check_param_arr_quads(left_operand,inicio)
    Quadruples.PilaDato.append(left_operand)
    Quadruples.PilaDato.append(right_operand)
    Quadruples.check_top_poper('parameter', p.lineno(-1))

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

def p_the_final_cut(p):
    '''
    the_final_cut : empty
    '''
    #tabla_varibles.get_constant_table()

def p_muere(p):
    '''
    muere : empty
    '''
    #tabla_varibles.get_constant_table()
    print("Quadruplos")
    conta = 0
    with open('JSON/datasss.json', 'w') as outfile:
        json.dump(tabla_varibles.diccionario, outfile)
    for q in Quadruples.PQuad:
        print(conta,q.operator,q.left_operand,q.right_operand,q.result)
        conta += 1
    Quadruples.print_quad()

quads = Quadruples.PQuad
tabla = tabla_varibles.diccionario
parser = yacc.yacc()
