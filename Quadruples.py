import sys
import json
from SemanticCube import semantic
from SemanticCube import Operators
from Temporales import Temporales

operatos = Operators()

class Quadruple:
    def __init__(self, operator, left_operand, right_operand, result):
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result

class Quadruples():
    def __init__(self):

        self.PilaO = []
        self.PTypes = []
        self.POper = []
        self.PQuad = []
        self.PJumps = []
        self.PilaDato = []
        self.Temporales = Temporales()

    def print_quad(self):
        print("PRINT Stack")
        print("op")
        for x in range(len(self.PilaO)):
            print (self.PilaO[x]),
        print("tipo")
        for x in range(len(self.PTypes)):
            print (self.PTypes[x]),
        print("Poper")
        for x in range(len(self.POper)):
            print (self.POper[x]),
        print("PJumps")
        for x in range(len(self.PJumps)):
            print (self.PJumps[x]),
        print("PDATO")
        for x in range(len(self.PilaDato)):
            print (self.PilaDato[x]['name'])

    def create_return_temporal(self,vardato):
        left_operand = self.Temporales.get_new_simple(vardato['type'])
        quad = Quadruple('=', vardato['direccion'], None, left_operand['direccion'])
        self.PQuad.append(quad)
        self.PilaDato.append(left_operand)

    def check_top_poper(self, case, lineno):
        length = len(self.POper)
        if (length > 0):
            if (case == 'sumres'):
                if (self.POper[-1] in operatos.operator['aritmetic']['sumres']):
                    self.pop_poper(lineno)
            elif (case == 'muldiv'):
                if (self.POper[-1] in operatos.operator['aritmetic']['muldiv']):
                    self.pop_poper(lineno)
            elif (case == 'relational'):
                if (self.POper[-1] in operatos.operator['relational']):
                    self.pop_poper(lineno)
            elif (case == 'logical'):
                if (self.POper[-1] in operatos.operator['logical']):
                    self.pop_poper(lineno)
            elif (case == 'equal'):
                if (self.POper[-1] in operatos.operator['equal']):
                    self.pop_poper(lineno)
            elif (case == 'parameter'):
                self.pop_poper(lineno)
            elif (case == 'return'):
                self.pop_poper(lineno)
            elif (case == 'print'):
                self.pop_print()

    def pop_poper(self, lineno):
        right_operand = self.PilaDato.pop()
        left_operand = self.PilaDato.pop()
        operator = self.POper.pop()
        result_Type = semantic(left_operand['type'], right_operand['type'], operator)
        if (result_Type == 'errorbadop'):
            raise TypeError("Unable to assign operator: {} to types: {} , {}. At line: {}".format(operator, left_operand['type'], right_operand['type'], lineno))
        else:
            if(operator=="="):
                quad = Quadruple(operator, right_operand['direccion'], None, left_operand['direccion'])
            elif(operator=="parametro"):
                quad = Quadruple(operator, right_operand['direccion'], None, left_operand['direccion'])
            elif(operator=="return"):
                print("return")
                quad = Quadruple(operator, right_operand['direccion'], None, left_operand['direccion'])
            else:
                result = self.Temporales.get_new_simple(result_Type)
                self.PilaDato.append(result)
                quad = Quadruple(operator, left_operand['direccion'], right_operand['direccion'], result['direccion'])
            self.PQuad.append(quad)
            #if(operator=="="):
            #    quad = Quadruple(operator, right_operand['name'], "NONE", left_operand['name'])
            #elif(operator=="parametro"):
            #    quad = Quadruple(operator, right_operand['name'], "NONE", left_operand['name'])
            #else:
            #    resultName = "T"+str(self.temporales)
            #    self.temporales +=1
            #    result = {'name':resultName,'type':result_Type,'complex': "simple"}
            #    self.PilaDato.append(result)
            #    quad = Quadruple(operator, left_operand['name'], right_operand['name'], result['name'])
            #self.PQuad.append(quad)

    def get_variable_arr(self, dato, index, lineno):
        if(dato['complex']=="arr"):
            inferior = 0
            superior = dato['limites']['limite1']
            dirbase = dato['direccion']
            quad = Quadruple('VER', index, inferior, superior)
            self.PQuad.append(quad)
            result = self.Temporales.get_new_simple('int')
            quad = Quadruple('+', index, dirbase, result['direccion'])
            self.PQuad.append(quad)
            aux = result
            aux['name'] = "("+str(aux['name'])+")"
            aux['direccion'] = "("+str(aux['direccion'])+")"
            self.PilaDato.append(aux)
        else:
            raise TypeError("Variable {} is not an Array. At Line: {}".format(dato['name'], lineno))

    def checkpar(self):
        length = len(self.POper)
        if (length>0):
            if (self.POper[-1] == ')'):
                self.POper.pop()
                self.POper.pop()

    def pop_print(self):
        operand = self.PilaDato.pop()
        operator = self.POper.pop()
        quad = Quadruple(operator, None, None, operand['direccion'])
        self.PQuad.append(quad)

    def gotomain(self):
        quad = Quadruple('GOTO', 'MAIN', None, None)
        self.PQuad.append(quad)

    def check_gotomain(self):
        for index, aux in enumerate(self.PQuad):
            if(aux.operator == "GOTO" and aux.left_operand == "MAIN"):
                break
        self.PQuad[index].result = len(self.PQuad)

    def reset_temporales(self):
        self.Temporales.reset()

    def addgotof(self):
        dato = self.PilaDato.pop()
        if (dato['type'] != 'bool'):
            raise TypeError("Unable use expresion as condition")
        else:
            quad = Quadruple('gotof', dato['direccion'], None, None)
            self.PQuad.append(quad)
            self.PJumps.append(len(self.PQuad))

    def addgotov(self):
        dato = self.PilaDato.pop()
        if (dato['type'] != 'bool'):
            raise TypeError("Unable use expresion as condition")
        else:
            quadnum = self.PJumps.pop()
            quad = Quadruple('gotov', dato['direccion'], None, quadnum)
            self.PQuad.append(quad)

    def closegotodown(self):
        quadnum = self.PJumps.pop()
        jumpto = len(self.PQuad)
        self.PQuad[quadnum-1].result = jumpto

    def closegotoup(self):
        quadnum = self.PJumps.pop()
        jumpto = self.PJumps.pop()
        self.PQuad[quadnum-1].result = jumpto - 1

    def addgoto(self):
        quad = Quadruple('GOTO', None, None, None)
        self.PQuad.append(quad)
        quadnum = self.PJumps.pop()
        self.PJumps.append(len(self.PQuad))
        jumpto = len(self.PQuad)
        self.PQuad[quadnum-1].result = jumpto

    def addfuncid(self,funcid):
        quad = Quadruple('ERA', funcid, None, None)
        self.PQuad.append(quad)

    def addparams(self, params, lineno):
        contador = params.contador
        limite = params.length
        if(contador<limite):
            key = list(params.params.keys())[contador]
            aux_dic = dict(params.params[key])
            self.PilaDato.append(aux_dic)
            self.POper.append('parametro')
            params.contador = contador + 1
        else:
            raise TypeError("Exceeded parameters. \n Expected: {} Given: {}. \n At Line: {}".format(limite, contador + 1, lineno))

    def checkfunclenght(self, params, lineno):
        contador = params.contador
        limite = params.length
        if(contador<limite):
            raise TypeError("Missing parameters. \n Expected: {} Given: {}. \n At Line: {}".format(limite, contador, lineno))
        else:
            quad = Quadruple('GOSUB', params.name, None, None)
            self.PQuad.append(quad)

    def endproc(self):
        quad = Quadruple('ENDPROC', None, None, None)
        self.PQuad.append(quad)

    def get_position(self):
        return len(self.PQuad)

    def printTemporales(self):
        with open('JSON/temporales.json', 'w') as outfile:
            json.dump(self.Temporales.diccionario, outfile)

    def pop_poper2(self, tablavariables, scope):
        right_operand = self.PilaO.pop()
        right_Type = self.PTypes.pop()
        left_operand = self.PilaO.pop()
        left_Type = self.PTypes.pop()
        operator = self.POper.pop()
        result_Type = semantic(left_Type, right_Type, operator)
        right_operand = self.get_direccion(right_operand, right_Type, tablavariables, scope)
        #left_operand = self.test_memoria(left_operand, left_Type, memoria)
        if (result_Type == 'errorbadop'):
            raise TypeError("Unable to assign "+operator+" to types "+left_operand+", "+right_operand)
        elif (result_Type == 'errorbaddt'):
            raise TypeError("Incompatible Data Type")
        else:
            if(operator=="="):
                quad = Quadruple(operator, right_operand, None, left_operand)
            elif(operator=="parametro"):
                quad = Quadruple(operator, right_operand, None, left_operand)
            else:
                result ="T"+str(self.temporales)
                self.temporales +=1
                self.PilaO.append(result)
                #print("PushT--  "+self.PilaO[-1])
                self.PTypes.append(result_Type)
                quad = Quadruple(operator, left_operand, right_operand, result)
                self.printTemporales()
            self.PQuad.append(quad)
            #if(left_operand['complex'] == "simple"):
            #    if(operator=="="):
            #        if(left_operand['cons'] != True):
            #            quad = Quadruple(operator, right_operand['name'], "NONE", left_operand['name'])
            #        else:
            #            raise TypeError("Unable to rewrite cons. At line: {}".format(lineno))
            #    elif(operator=="parametro"):
            #        quad = Quadruple(operator, right_operand['name'], "NONE", left_operand['name'])
            #    else:
            #        result = self.Temporales.get_new_simple(result_Type)
            #        self.PilaDato.append(result)
            #        quad = Quadruple(operator, left_operand['name'], right_operand['name'], result['name'])
            #    self.PQuad.append(quad)
