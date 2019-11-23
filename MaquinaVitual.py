from Memoria import Memoria
from Memoria import MemoriaContador
import sys
import json
globalinicio = 10000
localinicio = 20000
constanteinicio = 30000
test = {'5000':45}
test2 = {'6000':7}

aux_memoria = {
    'global'  : {},
    'locales' : MemoriaContador(),
    'constantes' : {}
}
aux_memoria['locales'].insertar_funcion("main")
aux_memoria['locales'].insertar_funcion("funcion1")
contador = aux_memoria['locales'].contador - 1
aux_memoria['locales'].listaMemoria[0] = {'main':"TEST"}
aux_memoria['locales'].listaMemoria[1] = {'func2':"TEST"}
print(aux_memoria['locales'].listaMemoria[1])
aux_memoria['global'][5000] = test['5000']
aux_memoria['global'][6000] = test2['6000']
print(aux_memoria['global'])

print(aux_memoria)
class MaquinaVirtual:
    def __init__ (self):
        self.Memoria=Memoria()

        quadruplesList = []
        quadruplesList.append(['+',20001,20002,40001])
        quadruplesList.append(['=',40001,20002,10001])
        # ERA
        quadruplesList.append(['+',20001,20002,40001])
        quadruplesList.append(['=',40001,20002,10001])
        aux_memoria['global'][123] = test['5000']
        print(aux_memoria['global'])

    def checkaddress(self, tipo, lugar):
        return

    def funciones(self, quadruplesList,posicion):
        operator = quadruplesList[posicion][0]
        izquierda = quadruplesList[posicion][0]
        derecha = quadruplesList[posicion][0]
        resultado = quadruplesList[posicion][0]

        if (operator == '+'):
            print("HERE")
