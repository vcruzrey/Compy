import sys
from SemanticCube import semantic
from SemanticCube import Operators
sys.tracebacklimit = 0

operatos = Operators()

class Quadruple:
    def __init__(self, operator, left_operand, right_operand, result):
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result

class Quadruples():
    temporales=1
    def __init__(self):

        self.PilaO = []
        self.PTypes = []
        self.POper = []
        self.PQuad = []
        self.PJumps = []
        self.PilaDato = []

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

    def check_top_poper(self, case, lineno):
        length = len(self.POper)
        if (length > 0):
            if (case == 'sumres'):
                if (self.POper[-1] in operatos.operator['aritmetic']['sumres']):
                    self.pop_poper2(lineno)
            elif (case == 'muldiv'):
                if (self.POper[-1] in operatos.operator['aritmetic']['muldiv']):
                    self.pop_poper2(lineno)
            elif (case == 'relational'):
                if (self.POper[-1] in operatos.operator['relational']):
                    self.pop_poper2(lineno)
            elif (case == 'logical'):
                if (self.POper[-1] in operatos.operator['logical']):
                    self.pop_poper2(lineno)
            elif (case == 'equal'):
                if (self.POper[-1] in operatos.operator['equal']):
                    self.pop_poper2(lineno)
            elif (case == 'parameter'):
                self.pop_poper2(lineno)
            elif (case == 'print'):
                self.pop_print(tablavariables, scope)

    def pop_poper2(self, lineno):
        right_operand = self.PilaDato.pop()
        left_operand = self.PilaDato.pop()
        operator = self.POper.pop()
        result_Type = semantic(right_operand['type'], left_operand['type'], operator)
        if (result_Type == 'errorbadop'):
            raise TypeError("Unable to assign "+operator+" to types "+left_operand['name']+", "+right_operand['name'])
        elif (result_Type == 'errorbaddt'):
            raise TypeError("Incompatible Data Type")
        else:
            if(operator=="="):
                quad = Quadruple(operator, right_operand['name'], "NONE", left_operand['name'])
            elif(operator=="parametro"):
                quad = Quadruple(operator, right_operand['name'], "NONE", left_operand['name'])
            else:
                resultName = "T"+str(self.temporales)
                self.temporales +=1
                result = {'name':resultName,'type':result_Type}
                self.PilaDato.append(result)
                quad = Quadruple(operator, left_operand['name'], right_operand['name'], result['name'])
            self.PQuad.append(quad)

    def pop_poper(self, tablavariables, scope):
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
                quad = Quadruple(operator, right_operand, "NONE", left_operand)
            elif(operator=="parametro"):
                quad = Quadruple(operator, right_operand, "NONE", left_operand)
            else:
                result = "T"+str(self.temporales)
                self.temporales +=1
                self.PilaO.append(result)
                #print("PushT--  "+self.PilaO[-1])
                self.PTypes.append(result_Type)
                quad = Quadruple(operator, left_operand, right_operand, result)
            self.PQuad.append(quad)

    def checkpar(self):
        length = len(self.POper)
        if (length>0):
            if (self.POper[-1] == ')'):
                self.POper.pop()
                self.POper.pop()

    def pop_print(self):
        operand = self.PilaO.pop()
        Type = self.PTypes.pop()
        operator = self.POper.pop()
        quad = Quadruple(operator, "NONE", "NONE", operand)
        self.PQuad.append(quad)

    def addgotof(self):
        operand = self.PilaO.pop()
        type = self.PTypes.pop()
        if (type != 'bool'):
            raise TypeError("Unable use expresion as condition")
        else:
            quad = Quadruple('gotof', operand, None, None)
            self.PQuad.append(quad)
            self.PJumps.append(len(self.PQuad))

    def addgotov(self):
        operand = self.PilaO.pop()
        type = self.PTypes.pop()
        if (type != 'bool'):
            raise TypeError("Unable use expresion as condition")
        else:
            quadnum = self.PJumps.pop()
            quad = Quadruple('gotov', operand, None, quadnum)
            self.PQuad.append(quad)

    def closegotodown(self):
        quadnum = self.PJumps.pop()
        jumpto = len(self.PQuad) + 1
        self.PQuad[quadnum-1].result = jumpto

    def closegotoup(self):
        quadnum = self.PJumps.pop()
        jumpto = self.PJumps.pop()
        self.PQuad[quadnum-1].result = jumpto

    def addgoto(self):
        quad = Quadruple('goto', None, None, None)
        self.PQuad.append(quad)
        quadnum = self.PJumps.pop()
        self.PJumps.append(len(self.PQuad))
        jumpto = len(self.PQuad) + 1
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
            self.PilaO.append(aux_dic['id'])
            self.PTypes.append(aux_dic['type'])
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

    def gotomain(self):
        quad = Quadruple('GOTO', 'main', None, None)
        self.PQuad.append(quad)

    def get_variablearrdir(self, dato, index, lineno):
        if(dato['complex']=="array"):
            inferior = 0
            superior = dato['tamano']
            dirbase = dato['direccion']
            quad = Quadruple('VER', index, inferior, superior)
            self.PQuad.append(quad)
            resultName = "T"+str(self.temporales)
            quad = Quadruple('+', index, dirbase, resultName)
            self.PQuad.append(quad)
            resultName = "(T"+str(self.temporales)+")"
            result = {'name':resultName,'type':dato['type']}
            self.temporales +=1
            self.PilaDato.append(result)
        else:
            raise TypeError("Variable {} is not an Array. At Line: {}".format(dato['name'], lineno))
