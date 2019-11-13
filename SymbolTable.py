import sys

class SymbolTable:
    def __init__(self):
        self.diccionario ={'dirFunc':{}}

    def test(self, dato):
        print(dato.id)

    def prueba_error(self):
        error = ("La variable ya esta registrada")
        return error

    def create_table(self, name, scope):
        new_table = {
            'name': name,
            'scope': scope,
            'vars' : {},
            'cons' : {},
        }
        self.diccionario['dirFunc'][name] = new_table

    def insert_variable(self, dato, scope):
        self.lookup_variable(dato.id, dato.type, scope)
        new_variable = {
            'id': dato.id,
            'type': dato.type
        }


        self.diccionario['dirFunc'][scope]['vars'][dato.id] = new_variable

    def lookup_variable(self, id, type, scope):
        if id in self.diccionario['dirFunc'][scope]['vars'].keys():
            raise TypeError("Variable: {} already declared".format(id))
