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

    def check_top_poper(self, case):
        length = len(self.POper)
        if (length > 0):
            if (case == 'sumres'):
                if (self.POper[-1] in operatos.operator['aritmetic']['sumres']):
                    self.pop_poper()
            elif (case == 'muldiv'):
                if (self.POper[-1] in operatos.operator['aritmetic']['muldiv']):
                    self.pop_poper()
            elif (case == 'relational'):
                if (self.POper[-1] in operatos.operator['relational']):
                    self.pop_poper()
            elif (case == 'logical'):
                if (self.POper[-1] in operatos.operator['logical']):
                    self.pop_poper()
            elif (case == 'equal'):
                if (self.POper[-1] in operatos.operator['equal']):
                    self.pop_poper()
            elif (case == 'parameter'):
                self.pop_poper()
            elif (case == 'print'):
                self.pop_print()

    def pop_poper(self):
        right_operand = self.PilaO.pop()
        right_Type = self.PTypes.pop()
        left_operand = self.PilaO.pop()
        left_Type = self.PTypes.pop()
        operator = self.POper.pop()
        result_Type = semantic(left_Type, right_Type, operator)
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
