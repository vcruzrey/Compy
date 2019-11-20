import sys
from Contador import Contador

globalinicio = 10000
globalfin = 19999
localinicio = 20000
localfin = 20999
constanteinicio = 30000
constantefin = 30999

class Memoria:
    def __init__(self):
        self.diccionario ={'dirMem':{}}
        self.contador = {'contador':{}}

    def create_memoria(self, name):
        new_table = {
            'int' : {},
            'float' : {},
            'string' : {},
            'bool' : {},
        }
        self.diccionario['dirMem'][name] = new_table

        if(name == 'global'):
            inicio = 10000
        elif(name == 'constantes'):
            inicio = 20000
        else:
            inicio = 30000

        new_contador = {
            'name' : name,
            'inicio': inicio,
            'limite' : 999,
            'int' : inicio,
            'float' : inicio + 1000,
            'string' : inicio + 2000,
            'bool' : inicio + 3000,
        }
        self.contador['contador'][name] = new_contador

    def insert_id(self, dato, scope):
        print(aux_dato.name)
        direccion = self.contador['contador'][scope][dato.type]
        self.diccionario['dirMem'][scope][dato.type].update({dato.id:direccion})
        self.contador['contador'][scope][dato.type] += 1
