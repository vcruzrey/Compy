import sys

class SymbolTable:
    def __init__(self):
        self.diccionario ={'dirFunc':{}}

    def validdt(self, tipo):
        switch = {
            'int' : True,
            'string' : True,
            'float' : True,
            'bool' : True,
        }
        if not (switch.get(tipo, False)):
            raise TypeError("Variable Type: {} not valid.".format(tipo))


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

    def create_functiontable(self, tabla):
        self.lookup_functiontable(tabla)
        new_table = {
            'name': tabla.id,
            'scope': "funcion",
            'params' : {},
            'vars' : {},
            'cons' : {},
            'return var' : None
        }
        self.diccionario['dirFunc'][tabla.id] = new_table

    def lookup_functiontable(self, tabla):
        if tabla.id in self.diccionario['dirFunc'].keys():
            raise TypeError("Function: {} already exists.".format(tabla.id))
        if tabla.id in self.diccionario['dirFunc']['global']['vars'].keys():
            raise TypeError("Function: {} already declared as global.".format(tabla.id))
        if tabla.id in self.diccionario['dirFunc']['global']['cons'].keys():
            raise TypeError("Function: {} already declared as global.".format(tabla.id))

    def insert_variable(self, dato, scope):
        new_variable = {
            'id': dato.id,
            'type': dato.type,
            'complex': dato.complex
        }
        if (dato.parameter):
            self.lookup_variablefunc(dato, scope)
            self.diccionario['dirFunc'][scope]['params'][dato.id] = new_variable
        else:
            self.lookup_variable(dato, scope)
            if (dato.cons):
                self.diccionario['dirFunc'][scope]['cons'][dato.id] = new_variable
            else:
                self.diccionario['dirFunc'][scope]['vars'][dato.id] = new_variable

    def lookup_variable(self, dato, scope):
        if dato.id in self.diccionario['dirFunc'][scope]['vars'].keys():
            raise TypeError("Variable: {} already declared in same scope ({})".format(dato.id, scope))
        if dato.id in self.diccionario['dirFunc'][scope]['cons'].keys():
            raise TypeError("Variable: {} already declared in same scope ({})".format(dato.id, scope))
        if dato.id in self.diccionario['dirFunc']['global']['vars'].keys():
            raise TypeError("Variable: {} already declared as global".format(dato.id))
        if dato.id in self.diccionario['dirFunc']['global']['cons'].keys():
            raise TypeError("Variable: {} already declared as global".format(dato.id))
        if (scope != 'global' and scope != 'main'):
            if dato.id in self.diccionario['dirFunc'][scope]['params'].keys():
                raise TypeError("Variable: {} already declared as parameter".format(dato.id))


    def lookup_variablefunc(self, dato, scope):
        if dato.id in self.diccionario['dirFunc']['global']['vars'].keys():
            raise TypeError("Variable: {} already declared as global".format(dato.id))
        if dato.id in self.diccionario['dirFunc']['global']['cons'].keys():
            raise TypeError("Variable: {} already declared as global".format(dato.id))
        if dato.id in self.diccionario['dirFunc'][scope]['params'].keys():
            raise TypeError("Variable: {} already declared as parameter".format(dato.id))

    def get_variableinfo(self, aux_dato, scope):
        if aux_dato in self.diccionario['dirFunc']['global']['vars'].keys():
            return self.diccionario['dirFunc']['global']['vars'][aux_dato]
        elif aux_dato in self.diccionario['dirFunc']['global']['cons'].keys():
            return self.diccionario['dirFunc']['global']['cons'][aux_dato]
        elif aux_dato in self.diccionario['dirFunc'][scope]['vars'].keys():
            return self.diccionario['dirFunc'][scope]['vars'][aux_dato]
        elif aux_dato in self.diccionario['dirFunc'][scope]['cons'].keys():
            return self.diccionario['dirFunc'][scope]['cons'][aux_dato]
        elif (scope != 'global' and scope != 'main'):
            if aux_dato in self.diccionario['dirFunc'][scope]['params'].keys():
                return self.diccionario['dirFunc'][scope]['params'][aux_dato]
        else:
            raise TypeError("Variable: {} hasnt been declared".format(aux_dato))
