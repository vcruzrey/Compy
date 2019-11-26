from Memoria import Memoria
from Quadruples import Quadruple
import operator
import sys
import json

aux_memoria = Memoria()
matematicas = ['+', '-', '*', '/','^','==', '!=', '>', '<', '>=', '<=','&&', '||','%','!']
#Globales 10000
#Constantes 20000
#Locales 30000

#Int 0 - 999
#FLoat 1000- 1999
#String 2000-2999
#Bool 3000-3999
class MaquinaVirtual:
    def __init__ (self, dirFunc, Quadruples):
        self.quadruplesList = Quadruples
        self.dirFunc = dict(dirFunc)
        self.posicion = 0
        #Quadruplos desde Main
        #self.quadruplesList.append(['=',20000,None,30000])
        #self.quadruplesList.append(['=',21000,None,31000])
        #self.quadruplesList.append(['<',20002,20000,33000])
        #self.quadruplesList.append(['=',33000,None,33001])
        #self.quadruplesList.append(['>',30000,20003,33002])
        #self.quadruplesList.append(['gotof',33002,None,10])#not sure si jala
        #self.quadruplesList.append(['^',31000,30000,31001])
        #self.quadruplesList.append(['print', None, None, 31001])
        #self.quadruplesList.append(['-',30000,20004,30000])
        #self.quadruplesList.append(['goto', None, None,4])
        #self.quadruplesList.append(['print',None, None, 31000])
        #self.quadruplesList.append(['print',None, None, 30000])

        #Escribir Constantes
        #aux_memoria.diccionario['constante'][20000] = 2
        #aux_memoria.diccionario['constante'][21000] = 1.0
        #aux_memoria.diccionario['constante'][20002] = 0
        #aux_memoria.diccionario['constante'][20003] = 1
        #aux_memoria.diccionario['constante'][20004] = 1


        #Ejemplos Escritura
        #aux_memoria.diccionario['global'][5000] = int(4)

        #contador = aux_memoria.diccionario['local'].contador
        #aux_memoria.diccionario['local'].actual[contador][3000] = int(4)

       #Lectura / Asignacion
        #print(aux_memoria.diccionario['constante'])
        #prueba_regreso = aux_memoria.diccionario['constante'][5000]
        #print(prueba_regreso)
        #print(aux_memoria.diccionario['local'].actual[contador])
        self.test()

    def test(self):
        print("HERE")
        test = self.quadruplesList[0].operator
        print(test)

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
                "|" :  operator.or_,
                "<" : operator.lt,
                ">" : operator.gt,
                "%" : operator.mod,
                "!" : operator.not_,
                "^" : operator.pow,
                ">=" : operator.ge,
                "<=" : operator.le,
                "==" : operator.eq,
                "!=" : operator.ne,

            }
            func_op = operations_switch[operator2]
            print(operator2)
            res = func_op(self.get_value(mem_izq, izquierda), self.get_value(mem_der, derecha))
            self.set_value(mem_res, resultado, res)
            self.posicion += 1

        elif (operator2 == '='):
            print ("equals")
            res  = self.get_value(mem_izq, izquierda)
            self.set_value(mem_res, resultado, res)
            self.posicion += 1


        #CHECAR QUE JALE ESTE EN ESPECIFICO
       # elif (operator == '!'):
        #    print("not")
          #  posicion += 1
         #   resultado = not derecha

        elif (operator2 == 'print'):
            print("print")
            res  = self.get_value(mem_res, resultado)
            print(res)
            self.posicion += 1

        #FALTAN POR DEFINIR
        elif (operator2 == 'gotof'):
            print("gotof")
            res  = self.get_value(mem_izq, izquierda)
            if (res):
                self.posicion += 1
                print("here")
            else:
                self.posicion = resultado

        elif (operator2 == 'gotov'):
            print('gotov')
            self.posicion = resultado

        elif (operator2 == 'goto'):
            print('goto')
            self.posicion = resultado

        elif (operator2 == 'GOSUB'):
            print("gosub")

        elif (operator2  == 'ERA'):
            print("era")

        elif (operator2 == 'ENDPROC'):
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


#aux_memoria.diccionario['local'].insertar_funcion("Func")
#self.quadruplesList.append(['+',10000,10001,30000])
#test.funciones()
#print(aux_memoria.diccionario)
#print(aux_memoria.diccionario['local'].actual[0])
#print(aux_memoria.diccionario['local'].actual[1])
