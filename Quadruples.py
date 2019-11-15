import sys
from SemanticCube import semantic
sys.tracebacklimit = 0

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

    def print_quad(self):
        print("HERE PRINT Stack")
        print("op")
        for x in range(len(self.PilaO)):
            print (self.PilaO[x]),
        print("tipo")
        for x in range(len(self.PTypes)):
            print (self.PTypes[x]),
        print("Poper")
        for x in range(len(self.POper)):
            print (self.POper[x]),

    def checksum(self):
        length = len(self.POper)
        if (length>0):
            if (self.POper[-1] == '+' or self.POper[-1] == '-'):
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
                    result = "T"+str(self.temporales)
                    self.temporales +=1
                    quad = Quadruple(operator, left_operand, right_operand, result)
                    self.PQuad.append(quad)
                    self.PilaO.append(result)
                    print("PushT--  "+self.PilaO[-1])
                    self.PTypes.append(result_Type)

    def checkmult(self):
        length = len(self.POper)
        if (length>0):
            if (self.POper[-1] == '*' or self.POper[-1] == '/'):
                print("ENTRO checkmult")
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
                    result = "T"+str(self.temporales)
                    self.temporales +=1
                    quad = Quadruple(operator, left_operand, right_operand, result)
                    self.PQuad.append(quad)
                    self.PilaO.append(result)
                    print("PushT--  "+self.PilaO[-1])
                    self.PTypes.append(result_Type)

    def checkrelop(self):
        length = len(self.POper)
        if (length>0):
            if (self.POper[-1] == "!="):
                print("ENTRO checkrelop")
                right_operand = self.PilaO.pop()
                right_Type = self.PTypes.pop()
                left_operand = self.PilaO.pop()
                left_Type = self.PTypes.pop()
                operator = self.POper.pop()
                print(operator+ "OPERTOR")
                result_Type = semantic(left_Type, right_Type, operator)
                if (result_Type == 'errorbadop'):
                    raise TypeError("Unable to assign "+operator+" to types "+left_operand+", "+right_operand)
                elif (result_Type == 'errorbaddt'):
                    raise TypeError("Incompatible Data Type")
                else:
                    result = "T"+str(self.temporales)
                    self.temporales +=1
                    quad = Quadruple(operator, left_operand, right_operand, result)
                    self.PQuad.append(quad)
                    self.PilaO.append(result)
                    print("PushT--  "+self.PilaO[-1])
                    self.PTypes.append(result_Type)

    def checkpar(self):
        length = len(self.POper)
        if (length>0):
            if (self.POper[-1] == ')'):
                print("ENTRO checkpar")
                self.POper.pop()
                self.POper.pop()
