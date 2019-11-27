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
        self.guardar_posicion = 0
        self.insert_constant_to_memory()
        self.funciones()

    def insert_constant_to_memory(self):
        for key in self.dirFunc['dirFunc']['constantes']['vars']:
            value = self.dirFunc['dirFunc']['constantes']['vars'][key]
            aux_memoria.diccionario['constante'][value['direccion']] = value['name']

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
        quadruples_length = len(self.quadruplesList)
        while(quadruples_length>self.posicion):
            posicion = self.posicion
            #print(self.quadruplesList[posicion].operator,self.quadruplesList[posicion].left_operand,self.quadruplesList[posicion].right_operand,self.quadruplesList[posicion].result)
            operation = self.quadruplesList[posicion].operator
            #print("operation")
            izquierda = self.quadruplesList[posicion].left_operand
            #print("izquierda")
            derecha = self.quadruplesList[posicion].right_operand
            #print("derecha")
            resultado = self.quadruplesList[posicion].result
            #print("resultado")

            mem_izq = self.posicion_direccion(izquierda)
            #print("mem_izq")
            mem_der = self.posicion_direccion(derecha)
            #print("mem_der")
            mem_res = self.posicion_direccion(resultado)
            #print("mem_res")

            if (operation in matematicas):
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
                func_op = operations_switch[operation]
                res = func_op(self.get_value(mem_izq, izquierda), self.get_value(mem_der, derecha))
                self.set_value(mem_res, resultado, res)
                self.posicion += 1

            elif (operation == '='):
                #print("equals")
                res  = self.get_value(mem_izq, izquierda)
                self.set_value(mem_res, resultado, res)
                #print(res)
                self.posicion += 1

            elif (operation == 'return'):
                #print("equals")
                res  = self.get_value(mem_res, resultado)
                self.set_value(mem_izq, izquierda, res)
                self.posicion += 1

            elif (operation == 'print'):
                #print("#print")
                res  = self.get_value(mem_res, resultado)
                print(res)
                self.posicion += 1

            elif (operation == 'GOTO'):
                self.posicion = resultado

            elif (operation == 'ENDPROC'):
                aux_memoria.diccionario['local'].liberar_funcion()
                self.posicion = self.guardar_posicion
                self.guardar_posicion = 0
                
            elif (operation == 'GOSUB'):
                print("GOSUB")
                aux_memoria.diccionario['local'].memoria_nueva()
                direccion = self.dirFunc['dirFunc'][izquierda]['inicio']
                self.guardar_posicion = self.posicion + 1
                self.posicion = direccion
                print(direccion)

            elif (operation  == 'ERA'):
                aux_memoria.diccionario['local'].insertar_funcion()
                aux_memoria.diccionario['local'].memoria_pasada()
                self.posicion += 1
                print("era end")

            elif (operation  == 'parametro'):
                res  = self.get_value(mem_izq, izquierda)
                aux_memoria.diccionario['local'].memoria_nueva()
                self.set_value(mem_res, resultado, res)
                aux_memoria.diccionario['local'].memoria_pasada()
                self.posicion += 1
                print(self.posicion)
                print("parametro")
                #aux_memoria.memoria_nueva()

                #aux_memoria.memoria_pasada()
        print("FINISH")

    def posicion_direccion(self,dir):
        if(isinstance(dir,int)):
            if (dir < 20000):
                return 'global'
            elif (dir < 30000):
                return 'constante'
            else:
                return 'local'
        else:
            return None


#aux_memoria.diccionario['local'].insertar_funcion("Func")
#self.quadruplesList.append(['+',10000,10001,30000])
#test.funciones()
##print(aux_memoria.diccionario)
##print(aux_memoria.diccionario['local'].actual[0])
##print(aux_memoria.diccionario['local'].actual[1])

        #Quadruplos desde Main
        #self.quadruplesList.append(['=',20000,None,30000])
        #self.quadruplesList.append(['=',21000,None,31000])
        #self.quadruplesList.append(['<',20002,20000,33000])
        #self.quadruplesList.append(['=',33000,None,33001])
        #self.quadruplesList.append(['>',30000,20003,33002])
        #self.quadruplesList.append(['gotof',33002,None,10])#not sure si jala
        #self.quadruplesList.append(['^',31000,30000,31001])
        #self.quadruplesList.append(['#print', None, None, 31001])
        #self.quadruplesList.append(['-',30000,20004,30000])
        #self.quadruplesList.append(['goto', None, None,4])
        #self.quadruplesList.append(['#print',None, None, 31000])
        #self.quadruplesList.append(['#print',None, None, 30000])

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
        ##print(aux_memoria.diccionario['constante'])
        #prueba_regreso = aux_memoria.diccionario['constante'][5000]
        ##print(prueba_regreso)
        ##print(aux_memoria.diccionario['local'].actual[contador])
