from collections import Counter
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
        self.pilaSaltos =[]
        self.insert_constant_to_memory()
        print("INICIO ---------- ------------------------------")
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
            #print("QUAD")
            #print(self.quadruplesList[posicion].operator,self.quadruplesList[posicion].left_operand,self.quadruplesList[posicion].right_operand,self.quadruplesList[posicion].result)
            operation = self.quadruplesList[posicion].operator
            #print("operation " + str(operation))
            izquierda = self.check_parentesis(self.quadruplesList[posicion].left_operand)
            #print("izquierda " + str(izquierda))
            derecha = self.check_parentesis(self.quadruplesList[posicion].right_operand)
            #print("derecha " + str(derecha))
            resultado = self.check_parentesis(self.quadruplesList[posicion].result)
            #print("resultado " + str(resultado))
            mem_izq = self.posicion_direccion(izquierda)
            #print(mem_izq)
            mem_der = self.posicion_direccion(derecha)
            #print(mem_der)
            mem_res = self.posicion_direccion(resultado)
            #print(mem_res)
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
                #print(str(self.get_value(mem_izq, izquierda)) +" +" + str(self.get_value(mem_der, derecha)))
                res = func_op(self.get_value(mem_izq, izquierda), self.get_value(mem_der, derecha))
                self.set_value(mem_res, resultado, res)
                self.posicion += 1

            elif (operation == 'gotof'):
                #print("gotof")
                res  = self.get_value(mem_izq, izquierda)
                if (res):
                    self.posicion += 1
                    #print("here")
                else:
                    self.posicion = resultado

            elif (operation == 'gotov'):
                #print("gotof")
                res  = self.get_value(mem_izq, izquierda)
                if (res):
                    self.posicion = resultado
                    #print("here")
                else:
                    self.posicion += 1

            elif (operation == '='):
                res  = self.get_value(mem_izq, izquierda)
                self.set_value(mem_res, resultado, res)
                #print(res)
                self.posicion += 1

            elif (operation == 'return'):
                #print("equals")
                res  = self.get_value(mem_res, resultado)
                self.set_value(mem_izq, izquierda, res)
                #print("RES "+str(res))
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
                self.posicion = self.pilaSaltos.pop()
                #print("ENDPRCO ------------------------ " + str(self.posicion))

            elif (operation == 'GOSUB'):
                #print("GOSUB")
                aux_memoria.diccionario['local'].memoria_nueva()
                direccion = self.dirFunc['dirFunc'][izquierda]['inicio']
                self.pilaSaltos.append(self.posicion + 1)
                self.posicion = direccion
                #print(direccion)

            elif (operation  == 'ERA'):
                aux_memoria.diccionario['local'].insertar_funcion()
                aux_memoria.diccionario['local'].memoria_pasada()
                self.posicion += 1
                #print("era end")

            elif (operation  == 'VER'):
                if(izquierda >= derecha and izquierda <= resultado):
                    self.posicion += 1
                    posicion = self.posicion
                    izquierda = self.check_parentesis(self.quadruplesList[posicion].left_operand)
                    derecha = self.check_parentesis(self.quadruplesList[posicion].right_operand)
                    resultado = self.check_parentesis(self.quadruplesList[posicion].result)
                    mem_res = self.posicion_direccion(resultado)
                    res = derecha + izquierda
                    self.set_value(mem_res, resultado, res)
                    self.posicion += 1
                else:
                    print("Error. Out of bounds")
                    self.posicion += 10000000
                #print("era end")

            elif (operation  == 'parametro'):
                if (derecha == None):
                    res  = self.get_value(mem_izq, izquierda)
                    aux_memoria.diccionario['local'].memoria_nueva()
                    self.set_value(mem_res, resultado, res)
                    aux_memoria.diccionario['local'].memoria_pasada()
                    self.posicion += 1
                else:
                    for i in range(derecha):
                        res  = self.get_value(mem_izq, izquierda + i)
                        aux_memoria.diccionario['local'].memoria_nueva()
                        self.set_value(mem_res, resultado + i, res)
                        aux_memoria.diccionario['local'].memoria_pasada()
                    self.posicion += 1

            elif (operation  == 'arr'):
                self.posicion += 1

            elif (operation  == 'len'):
                self.set_value(mem_res, resultado, derecha)
                self.posicion += 1

            elif (operation  == 'str'):
                res  = self.get_value(mem_izq, izquierda)
                self.set_value(mem_res, resultado, str(res))
                self.posicion += 1

            elif (operation  == 'FSP'):
                pila_aux = []
                while operation != "FSPEND":
                    if (derecha == None):
                        res  = self.get_value(mem_res, resultado)
                        pila_aux.append(res)
                        self.posicion += 1
                    else:
                        for i in range(derecha):
                            res  = self.get_value(mem_res, resultado + i)
                            pila_aux.append(res)
                        self.posicion += 1
                    posicion = self.posicion
                    operation = self.quadruplesList[posicion].operator
                    derecha = self.check_parentesis(self.quadruplesList[posicion].right_operand)
                    resultado = self.check_parentesis(self.quadruplesList[posicion].result)
                    mem_der = self.posicion_direccion(derecha)
                    mem_res = self.posicion_direccion(resultado)
                res_aux = self.funciones_especiales(pila_aux, izquierda)
                mem_res = self.posicion_direccion(resultado)
                self.set_value(mem_res, resultado, res_aux)
                self.posicion += 1
                #print(self.posicion)
                #print("parametro")
                #aux_memoria.memoria_nueva()

                #aux_memoria.memoria_pasada()
        #print(aux_memoria.diccionario['local'].actual[0])
        print("FINISH")

    def funciones_especiales(self, pila, tipo):
        if tipo == "average":
            n = len(pila)
            get_sum = sum(pila)
            avr = get_sum / n
            return avr
        elif tipo == "median":
            n = len(pila)
            pila.sort()
            if n % 2 == 0:
                 median1 = pila[n//2]
                 median2 = pila[n//2 - 1]
                 median = (median1 + median2)/2
            else:
                median = pila[n//2]
            return median
        elif tipo == "mode":
            n = len(pila)
            data = Counter(pila)
            get_mode = dict(data)
            mode = [k for k, v in get_mode.items() if v == max(list(data.values()))]
            if len(mode) == n:
                get_mode = -1
            else:
                get_mode = ', '.join(map(str, mode))
            return get_mode
    def check_parentesis(self, dir):
        test = str(dir)
        if(test[0]=="("):
            apunta = int(dir[1:-1])
            mem_apunta = self.posicion_direccion(apunta)
            res = self.get_value(mem_apunta, apunta)
            return res
        return dir

    def posicion_direccion(self,dir):
        if(isinstance(dir,int)):
            if (dir<1000):
                return None
            elif (dir < 20000):
                return 'global'
            elif (dir < 30000):
                return 'constante'
            else:
                return 'local'
        else:
            return None
