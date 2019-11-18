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
            if(operator!="="):
                result = "T"+str(self.temporales)
                self.temporales +=1
                self.PilaO.append(result)
                #print("PushT--  "+self.PilaO[-1])
                self.PTypes.append(result_Type)
                quad = Quadruple(operator, left_operand, right_operand, result)
            else:
                quad = Quadruple(operator, right_operand, "NONE", left_operand)
            self.PQuad.append(quad)

    def checkpar(self):
        length = len(self.POper)
        if (length>0):
            if (self.POper[-1] == ')'):
                self.POper.pop()
                self.POper.pop()

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
