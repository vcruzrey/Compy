import sys

class Memoria:
    def __init__(self):
        self.directorio = {
            'int' : {},
            'float' : {},
            'string' : {},
            'bool' : {},
        }

class MemoriaContador:
    def __init__(self):
        self.listaMemoria = [{}]
        self.contador = 0

    def insertar_funcion(self, nombre):
        self.listaMemoria.append({})
        self.contador += 1
