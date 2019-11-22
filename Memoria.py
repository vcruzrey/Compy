import sys
from Contador import Contador

class Memoria:
    def __init__(self):
        self.diccionario ={'dirMem':{}}
        self.contador={}
    def create_memoria(self, name):
        new_table = {
            'int' : {},
            'float' : {},
            'string' : {},
            'bool' : {},
        }

    def insert_id(self, dato, scope):
        direccion = self.contador['contador'][scope][dato.type]
        self.diccionario['dirMem'][scope][dato.type].update({dato.id:direccion})
        self.contador['contador'][scope][dato.type] += 1

    def insert_constant(self, name, type, scope):
        direccion = self.contador['contador'][scope][type]
        self.diccionario['dirMem'][scope][type].update({name:direccion})
        self.contador['contador'][scope][type] += 1
