import sys

class MemoriaContador:
    def __init__(self):
        self.actual = [{}]
        self.contador = 0
        
    def insertar_funcion(self, nombre):
        self.actual.append({})
        self.contador += 1

class Memoria:
    def __init__(self):
        self.diccionario = {
            'global'  : {},
            'local' : MemoriaContador(),
            'constante' : {}
        }