import sys

class MemoriaContador:
    def __init__(self):
        self.actual = [{}]
        self.contador = 0

    def insertar_funcion(self):
        self.actual.append({})
        self.contador += 1

    def memoria_pasada(self):
        self.contador -= 1

    def memoria_nueva(self):
        self.contador += 1

    def liberar_funcion(self):
        self.actual.pop()
        self.contador -= 1

class Memoria:
    def __init__(self):
        self.diccionario = {
            'global'  : {},
            'local' : MemoriaContador(),
            'constante' : {}
        }
