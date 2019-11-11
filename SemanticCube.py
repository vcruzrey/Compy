#OPERATORS
aritmetic = ['+', '-', '*', '/','^']
booleanOp = ['==', '!=', '>', '<', '>=', '<=']
math = ['pi','%']
equal = '='
logicalOp = ['&&', '||']

#SEMANTIC CUBE FUNCTION: defines what value is returned from an operation of two types of data
def semantic(left, right, operator):
    #INTEGERS
    if(left == 'int'):
        #INT - INT
        if(right == 'int'):
            if(operator in aritmetic or operator == equal):
                return 'int'
            elif(operator in math):
                return 'float'
            elif(operator in booleanOp):
                return 'bool'
            else:
                return 'error'
        #INT - FLOAT
        elif(right == 'float'):
            if(operator in aritmetic or math):
                return 'float'
            elif(operator in booleanOp):
                return 'bool'
            else:
                return 'error'
        else:
            return 'error'
    #FLOATS
    elif(left == 'float'):
        #FLOAT - FLOAT
        if(right == 'float'):
            if(operator in aritmetic or operator == equal or operator in math):
                return 'float'
            elif(operator in booleanOp):
                return 'bool'
            else:
                return 'error'
        #FLOAT - INT  
        elif(right == 'int'):
            if(operator in aritmetic or operator in math):
                return 'float'
            elif(operator in booleanOp):
                return 'bool'
            else:
                return 'error'
        else:
            return 'error'
    #STRINGS
    elif(left == 'string'):
        if(right == 'string'):
            if(operator == equal):
                return 'string'
            elif(operator == '==' or operator == '!='):
                return 'bool'
            #concatenacion de strings
            elif(operator == '+'):
                return 'string'
            else:
                return 'error'
        else:
            return 'error'
    #BOOLEANS
    elif(left == 'bool'):
        if(right == 'bool'):
            if(operator == equal or operator == '==' or operator in logicalOp or  operator == '!='):
                return 'bool'
            else:
                return 'error'
        else:
            return 'error'

    else:
        return 'error'