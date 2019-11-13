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
    def __init__(self):

        self.PilaO = []
        self.PTypes = []
        self.POper = []

    def print_quad(self):
        print("HERE PRINT Stack")
        for x in range(len(self.PilaO)):
            print (self.PilaO[x]),

        for x in range(len(self.PTypes)):
            print (self.PTypes[x]),

        for x in range(len(self.POper)):
            print (self.POper[x]),

    def checksum(self):
        length = len(self.POper)
        if (length>0):
            if (self.POper[length-1] == '+' or '-'):
                right_operand = self.PilaO.pop()
                left_operand = self.PilaO.pop()
                right_Type = self.PTypes.pop()
                left_Type = self.PTypes.pop()
                operator = self.POper.pop()
                result_Type = semantic(left_Type, right_Type, operator)
                if (result_Type == 'errorbadop'):
                    raise TypeError("Unable to assign "+operator+" to types "+left_operand+", "+right_operand)
                elif (result_Type == 'errorbaddt'):
                    raise TypeError("Incompatible Data Type")
                else:
                    result = "Temporal"
                    quadruple = Quadruple(operator, left_operand, right_operand, result)
                    print(operator)
                    print(left_operand)
                    print(right_operand)
                    print(result)
                    self.PilaO.append(result)
                    self.PTypes.append('int')

    #Rolando- MultDiv
    def checkmult(self):
        length = len(self.POper)
        if (length>0):
            if (self.POper[length-1] == '*' or '/'):
                right_operand = self.PilaO.pop()
                left_operand = self.PilaO.pop()
                right_Type = self.PTypes.pop()
                left_Type = self.PTypes.pop()
                operator = self.POper.pop()
                result_Type = semantic(left_Type, right_Type, operator)
                if (result_Type == 'errorbadop'):
                    raise TypeError("Unable to assign "+operator+" to types "+left_operand+", "+right_operand)
                elif (result_Type == 'errorbaddt'):
                    raise TypeError("Incompatible Data Type")
                else:
                    result = "Temporal"
                    quadruple = Quadruple(operator, left_operand, right_operand, result)
                    print(operator)
                    print(left_operand)
                    print(right_operand)
                    print(result)
                    self.PilaO.append(result)
                    self.PTypes.append('int')
