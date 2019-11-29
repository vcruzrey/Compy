# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required

tokens = [
    'ID',

    #Data Types
    'DTI', #int
    'DTF', #float
    'DTS', #string
    'DTSIP', #string con interpolacion

    #Arithmetic Operators
    'EQUALS',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'POWER',
    'MODULE',

    #Logical Operators
    'AND',
    'OR',
    'NOT',

    #Relational Operators
    'GREATER',
    'LOWER',
    'SAME',
    'LEQUAL',
    'GEQUAL',
    'NOTEQUAL',

    #Structure
    'LPAREN',
    'RPAREN',
    'LBRCKT',
    'RBRCKT',
    'LCORCHO',
    'RCORCHO',
    'COMMA',
    'PNTCOMMA',
    'COLON',
    'POINT',
 ]

reserved = {

    #Data Type
    'int' : 'INT',
    'float' : 'FLOAT',
    'bool' : 'BOOL',
    'string' : 'STRING',
    'void' : 'VOID',
    'cons' : 'CONS',
    'False' : 'FALSE',
    'True' : 'TRUE',

    #Data Structures
    'arr' : 'ARR',
    'mat' : 'MAT',

    #Structure
    'main' : 'MAIN',
    'func' : 'FUNC',
    'return' : 'RETURN',
    #Print
    'print' : 'PRINT',

    #Conditions
    'if' : 'IF',
    'else' : 'ELSE',
    'switch': 'SWITCH',
    'case' : 'CASE',
    'break' : 'BREAK',

    #Loops
    'while' : 'WHILE',
    'do' : 'DO',
    'for' : 'FOR',

    #Math Functions
    'sqrt' : 'SQRT',
    'mode' : 'MODE',
    'median' : 'MEDIAN',
    'average' : 'AVERAGE',
    'pi' : 'PI',
    'len' : 'LEN',
    'str' : 'STR',


    'end' : 'END',
}

tokens += list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_EQUALS  = r'\='
t_MINUS   = r'\-'
t_TIMES   = r'\*'
t_DIVIDE  = r'[/]'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_POWER   = r'\^'
t_RBRCKT  = r'\]'
t_LBRCKT  = r'\['
t_COMMA   = r'\,'
t_PNTCOMMA  = r'\;'
t_DTSIP = r'\".*(\$[a-zA-Z_][a-zA-Z_0-9]+\$)+.*\"'
t_DTS = r'\".*?\"'

t_AND = r'[&][&]'
t_OR = r'[|][|]'
t_LCORCHO = r'\{'
t_RCORCHO = r'\}'
t_COLON = r'\:'
t_POINT = r'\.'
t_GREATER = r'\>'
t_LOWER = r'\<'
t_SAME = r'\=\='
t_LEQUAL = r'\<\='
t_GEQUAL = r'\>\='
t_NOTEQUAL = r'\!\='
t_NOT = r'\!'
t_MODULE = r'\%'


# A regular expression rule with some action code
def t_DTF(t):
    r'(\d*\.\d+)|(\d+\.\d*)|(\-\d*\.\d+)|(\-\d+\.\d*)'
    t.value = float(t.value)
    return t

#Integer definition
def t_DTI(t):
    r'\d+|\-\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'ID')    # Check for reserved words
     return t


#def t_Comment(t):
#	r'[/][*][^*]*[*]+([^*/][^*]*[*]+)*[/] | [/][/].*'
#	pass

# Build the lexer
lexer = lex.lex()
