import sys
#OPERATORS
aritmetic = ['+', '-', '*', '/','^']
booleanOp = ['==', '!=', '>', '<', '>=', '<=']
math = ['pi','%']
equal = ['=','parametro']
logicalOp = ['&&', '||']

class Operators:
    def __init__(self):
        self.operator = {
            'aritmetic' : {
                'sumres': ['+','-'],
                'muldiv': ['*','/'],
            },
            'relational' : ['==', '!=', '>', '<', '>=', '<='],
            'math' : ['pi','%'],
            'equal' : ['=','parametro'],
            'logical' : ['&&', '||']
        }

#SEMANTIC CUBE FUNCTION: defines what value is returned from an operation of two types of data
def semantic(left, right, operator):

    #CHECAR CASO DEL NOT ANTES QUE CUALQUIER OTRA COMPARACIÓN
    if(right=='bool'):
        if (operator=='!'):
            return bool

    #INTEGERS
    elif(left == 'int'):
        #INT - INT
        if(right == 'int'):
            if(operator in aritmetic or operator in equal):
                return 'int'
            elif(operator in math):
                return 'float'
            elif(operator in booleanOp):
                return 'bool'
            else:
                return 'errorbadop'

        #INT - FLOAT
        elif(right == 'float'):
            if(operator in aritmetic or math):
                return 'float'
            elif(operator in booleanOp):
                return 'bool'
            else:
                return 'errorbadop'
        else:
            return 'errorbaddt int2'
    #FLOATS
    elif(left == 'float'):
        #FLOAT - FLOAT
        if(right == 'float'):
            if(operator in aritmetic or operator in equal or operator in math):
                return 'float'
            elif(operator in booleanOp):
                return 'bool'
            else:
                return 'errorbadop'
        #FLOAT - INT
        elif(right == 'int'):
            if(operator in aritmetic or operator in math):
                return 'float'
            elif(operator in booleanOp):
                return 'bool'
            else:
                return 'errorbadop'
        else:
            return 'errorbaddt'
    #STRINGS
    elif(left == 'string'):
        if(right == 'string'):
            if(operator in equal):
                return 'string'
            elif(operator == '==' or operator == '!='):
                return 'bool'
            #concatenacion de strings
            elif(operator == '+'):
                return 'string'
            else:
                return 'errorbadop'
        else:
            return 'errorbaddt'
    #BOOLEANS
    elif(left == 'bool'):
        if(right == 'bool'):
            if(operator == '=' or operator == '==' or operator in logicalOp or operator == '!='):
                return 'bool'
            else:
                return 'errorbadop'
        else:
            return 'errorbaddt'   

    else:
        raise TypeError("Unrecognized Data Type")

#print(semantic('bool','bool','!'))
