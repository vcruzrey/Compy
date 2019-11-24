import sys
#OPERATORS
aritmetic = ['+', '-', '*']
aritmeticcomplex = ['pi','%', '/','^']
relational = ['==', '!=', '>', '<', '>=', '<=']
logical = ['&&', '||']
equal = ['=','parametro']

#Missing operators
class Operators:
    def __init__(self):
        self.operator = {
            'aritmetic' : {
                'sumres': ['+','-'],
                'muldiv': ['*','/'],
            },
            'math' : ['pi','%'],
            'relational' : ['==', '!=', '>', '<', '>=', '<='],
            'equal' : ['=','parametro'],
            'logical' : ['&&', '||']
        }

def semantic(left, right, operator):

    #CHECAR CASO DEL NOT ANTES QUE CUALQUIER OTRA COMPARACIÓN
    #if(right=='bool'):
    #    if (operator=='!'):
    #        return bool

    if(left == 'int'):
        if(right == 'int'):
            if(operator in aritmetic or operator in equal):
                return 'int'
            elif(operator in aritmeticcomplex):
                return 'int'
            elif(operator in relational):
                return 'bool'
            else:
                return 'errorbadop'

        elif(right == 'float'):
            if(operator in aritmetic or operator in aritmeticcomplex):
                return 'float'
            elif(operator in relational):
                return 'bool'
            else:
                return 'errorbadop'
        else:
            return 'errorbadop'

    elif(left == 'float'):
        if(right == 'float'):
            if(operator in aritmetic or operator in aritmeticcomplex or operator in equal):
                return 'float'
            elif(operator in relational):
                return 'bool'
            else:
                return 'errorbadop'

        elif(right == 'int'):
            if(operator in aritmetic or operator in aritmeticcomplex):
                return 'float'
            elif(operator in relational):
                return 'bool'
            else:
                return 'errorbadop'
        else:
            return 'errorbadop'

    elif(left == 'string'):
        if(right == 'string'):
            if(operator in equal):
                return 'string'
            elif(operator == '==' or operator == '!='):
                return 'bool'
            elif(operator == '+'):
                return 'string'
            else:
                return 'errorbadop'

        elif(right == 'int' or right == 'float'):
            if(operator == '+'):
                return 'string'
            else:
                return 'errorbadop'
        else:
            return 'errorbadop'

    elif(left == 'bool'):
        if(right == 'bool'):
            if(operator in relational or operator in logical or operator in equal):
                return 'bool'
            else:
                return 'errorbadop'
        else:
            return 'errorbadop'
