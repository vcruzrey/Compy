class SymbolTable:
    def __init__(self):
        self.diccionario ={'dirFunc':{}}

    def test(self):
        print("here")

    def prueba_error(self):
        error = ("La variable ya esta registrada")
        return error

    def create_table(self, name, scope):
        new_table = {
            'name': name,
            'scope': scope,
            'vars' : {}
        }
        self.diccionario['dirFunc'][name] = new_table

    def insert_variable(self, id, type, scope):
        new_variable = {
            'id': id,
            'type': type
        }
        self.diccionario['dirFunc'][scope]['vars'][id] = new_variable
