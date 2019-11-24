from Memoria import Memoria
from Quadruples import Quadruple
import operator
import sys
import json

aux_memoria = Memoria()
matematicas = ['+', '*', '-', '/', '&&','<']
#Globales 10000
#Constantes 20000
#Locales 30000

#Int 0 - 999
#FLoat
#String 
#Bool
print(aux_memoria)
class MaquinaVirtual:
    def __init__ (self):
        self.quadruplesList = []
        self.posicion = 0
        #Quadruplos desde Main
        self.quadruplesList.append(['=',20000,None,10000])
        self.quadruplesList.append(['=',20001,None,10001])
        self.quadruplesList.append(['+',10000,10001,30000])
        self.quadruplesList.append(['=',30000,None,10002])
        #print 30000
        #a = 5
        #b = 7
        #c  = a + b

        #Escribir Constantes
        aux_memoria.diccionario['constante'][20000] = "hola"
        aux_memoria.diccionario['constante'][20001] = "  jesus"

        #Ejemplos Escritura
        #aux_memoria.diccionario['global'][5000] = int(4)
        
        #contador = aux_memoria.diccionario['local'].contador
        #aux_memoria.diccionario['local'].actual[contador][3000] = int(4)
        
       #Lectura / Asignacion
        #print(aux_memoria.diccionario['constante'])
        #prueba_regreso = aux_memoria.diccionario['constante'][5000]
        #print(prueba_regreso)
        #print(aux_memoria.diccionario['local'].actual[contador])

    def checkaddress(self, tipo, lugar):
        return

    def get_value(self, memoria, direccion):
        if(memoria == 'local'):
            contador = aux_memoria.diccionario['local'].contador
            return aux_memoria.diccionario[memoria].actual[contador][direccion]
        else:
            return aux_memoria.diccionario[memoria][direccion]
    
    def set_value(self, memoria, direccion, valor):
        if(memoria == 'local'):
            contador = aux_memoria.diccionario['local'].contador
            aux_memoria.diccionario[memoria].actual[contador][direccion] = valor
        else:
            aux_memoria.diccionario[memoria][direccion] = valor
    
    def funciones(self):
        operator2 = self.quadruplesList[self.posicion][0]
        izquierda = self.quadruplesList[self.posicion][1]
        derecha = self.quadruplesList[self.posicion][2]
        resultado = self.quadruplesList[self.posicion][3]
        
        mem_izq = self.posicion_direccion(izquierda)
        mem_der = self.posicion_direccion(derecha)
        mem_res = self.posicion_direccion(resultado)

        if (operator2 in matematicas): 
            operations_switch = {
                "+" : operator.add,
                "-" : operator.sub,
                "*" : operator.mul,
                "/" : operator.truediv,
                "&&" : operator.and_,
                "<" : operator.lt
            }
            func_op = operations_switch[operator2]
            print(func_op)
            res = func_op(self.get_value(mem_izq, izquierda), self.get_value(mem_der, derecha))
            self.set_value(mem_res, resultado, res)
            self.posicion += 1

        if (operator2 == '='):
            print ("equals")
            res  = self.get_value(mem_izq, izquierda)
            self.set_value(mem_res, resultado, res)
            self.posicion += 1            

        elif (operator == '%'):
            res = self.get_value(mem_izq, izquierda) % self.get_value(mem_der, derecha)
            self.set_value(mem_res, resultado, res)
            self.posicion += 1

        elif (operator == '^'):
            res = self.get_value(mem_izq, izquierda) ** self.get_value(mem_der, derecha)
            self.set_value(mem_res, resultado, res)
            self.posicion += 1

        elif(operator == '&&'):
            res = self.get_value(mem_izq, izquierda) and self.get_value(mem_der, derecha)
            self.set_value(mem_res, resultado, res)
            self.posicion += 1

        elif (operator == '|'):
            res = self.get_value(mem_izq, izquierda) + self.get_value(mem_der, derecha)
            self.set_value(mem_res, resultado, res)
            self.posicion += 1
        
        elif (operator == '>'):
            print("greather")
            resultado = izquierda > derecha
            posicion += 1

        elif (operator == '<'):
            print ("lower")
            resultado = izquierda < derecha
            posicion += 1

        elif (operator == '=='):
            print ("equal")
            resultado = izquierda == derecha
            posicion += 1
        
        elif (operator == '<='):
            print("loweq")
            resultado = izquierda <= derecha
            posicion += 1
        
        elif (operator == '>='):
            print("greq")
            resultado = izquierda >= derecha
            posicion +=1

        elif (operator == '!='):
            print("noteq")
            resultado = izquierda != derecha
            posicion +=1

        #CHECAR QUE JALE ESTE EN ESPECIFICO
        elif (operator == '!'):
            print("not")
            resultado = not derecha
            posicion += 1

        elif (operator == 'print'):
            print("print")
            print(resultado)
            posicion += 1

        #FALTAN POR DEFINIR
        elif (operator == 'gotof'):
            print("gotof")

        elif (operator == 'gotov'):
            print('gotov')

        elif (operator == 'goto'):
            print('goto')

        elif (operator == 'GOSUB'):
            print("gosub")
        
        elif (operator  == 'ERA'):
            print("era")

        elif (operator == 'ENDPROC'):
            print ("endproc")
        
    def posicion_direccion(self,dir): 
        if (dir == None):
            return None
        elif (dir < 20000):
            return 'global'
        elif (dir < 30000):  
            return 'constante'
        else: 
            return 'local'

test = MaquinaVirtual()
test.funciones()
test.funciones()
test.funciones()
test.funciones()
print(aux_memoria.diccionario)
print(aux_memoria.diccionario['local'].actual)
#aux_memoria.diccionario['local'].insertar_funcion("Func")
#self.quadruplesList.append(['+',10000,10001,30000])
#test.funciones()
#print(aux_memoria.diccionario)
#print(aux_memoria.diccionario['local'].actual[0])
#print(aux_memoria.diccionario['local'].actual[1])

