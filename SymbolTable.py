import sys
from Contador import Contador

globalinicio = 10000
localinicio = 20000
constanteinicio = 30000

class SymbolTable:
    def __init__(self):
        self.diccionario ={'dirFunc':{}}
        self.contador = {'contador':{}}

    def create_table_globalcons(self, name):
        if(name=='global'):
            inicio = 10000
        elif(name == 'constantes'):
            inicio = 30000

        new_table = {
            'name': name,
            'vars' : {},
        }
        self.diccionario['dirFunc'][name] = new_table

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

    def create_table_main(self):
        name = "main"
        inicio = 20000
        new_table = {
            'name': name,
            'inicio' : 0,
            'fin' : 0,
            'tamano' : 0,
            'vars' : {},
        }
        self.diccionario['dirFunc'][name] = new_table

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

    def create_functiontable(self, tabla):
        self.lookup_functiontable(tabla)
        new_table = {
            'name': tabla.name,
            'inicio' : 0,
            'fin' : 0,
            'tamano' : 0,
            'type' : tabla.type,
            'params' : {},
            'vars' : {},
            'return var' : None
        }
        self.diccionario['dirFunc'][tabla.name] = new_table

    def lookup_functiontable(self, tabla):
        if tabla.name in self.diccionario['dirFunc'].keys():
            raise TypeError("Function: {} already exists.".format(tabla.name))
        if tabla.name in self.diccionario['dirFunc']['global']['vars'].keys():
            raise TypeError("Function: {} already declared as global.".format(tabla.name))
        if tabla.name in self.diccionario['dirFunc']['global']['cons'].keys():
            raise TypeError("Function: {} already declared as global.".format(tabla.name))

    #NOT FINISHED
    def insert_variable(self, dato, tabla, lineno):
        scope = tabla.name
        self.lookup_variable(dato, scope, lineno)
        if (dato.complex == "simple"):
            direccion = self.create_direccion(dato, scope)
            new_variable = {
                'name': dato.name,
                'type': dato.type,
                'cons' : dato.cons,
                'complex': dato.complex,
                'direccion': direccion
            }
        else:
            dato.tamano, limites = self.create_complex_limits(dato)
            direccion = self.create_direccion(dato, scope)
            new_variable = {
                'name': dato.name,
                'type': dato.type,
                'complex': dato.complex,
                'tamano' : dato.tamano,
                'limites' : limites,
                'direccion': direccion
            }
        self.diccionario['dirFunc'][scope]['vars'][dato.name] = new_variable

    def create_direccion(self, dato, scope):
        direccion = self.contador['contador'][scope][dato.type]
        if(dato.complex == "simple"):
            self.contador['contador'][scope][dato.type] += 1
        else:
            self.contador['contador'][scope][dato.type] += dato.tamano
        return direccion


    def create_complex_limits(self, dato):
        if (dato.complex == "array"):
            tamano = dato.tamano[0] + 1
            return tamano, {'limite1' : tamano}
        elif (dato.complex == "matrix"):
            limite1 = dato.tamano[0]
            limite2 = dato.tamano[1]
            tamano = (limite1 + 1) * (limite2 + 1)
            m1 = int(tamano / (limite1 + 1))
            return tamano, {'limite1' : limite1, 'limite2' : limite2, 'm1' : m1}
        #if (dato.parameter):
        #    self.lookup_variablefunc(name, scope)
        #    self.diccionario['dirFunc'][scope]['params'][dato.id] = new_variable
        #else:
        #    self.lookup_variable(name, scope)
        #    self.diccionario['dirFunc'][scope]['vars'][dato.id] = new_variable

    def lookup_variable(self, dato, scope, lineno):
        name = dato.name
        if (scope == 'global'):
            if name in self.diccionario['dirFunc']['global']['vars'].keys():
                raise TypeError("Variable: {} already declared as global. At line: {}".format(dato.name, lineno))
        else:
            if name in self.diccionario['dirFunc'][scope]['vars'].keys():
                raise TypeError("Variable: {} already declared in same scope ({}). At line {}".format(dato.name, scope, lineno))
            elif name in self.diccionario['dirFunc']['global']['vars'].keys():
                raise TypeError("Variable: {} already declared as global. At line: {}".format(dato.name, lineno))
            #if (scope != 'global' and scope != 'main'):
            #    if dato.id in self.diccionario['dirFunc'][scope]['params'].keys():
            #        raise TypeError("Variable: {} already declared as parameter".format(dato.id))


    def lookup_variablefunc(self, dato, scope):
        if dato.id in self.diccionario['dirFunc']['global']['vars'].keys():
            raise TypeError("Variable: {} already declared as global".format(dato.id))
        if dato.id in self.diccionario['dirFunc']['global']['cons'].keys():
            raise TypeError("Variable: {} already declared as global".format(dato.id))
        if dato.id in self.diccionario['dirFunc'][scope]['params'].keys():
            raise TypeError("Variable: {} already declared as parameter".format(dato.id))

    def get_variableinfo(self, name, scope, lineno):
        if (scope == 'global'):
            if name in self.diccionario['dirFunc']['global']['vars'].keys():
                return self.diccionario['dirFunc']['global']['vars'][name]
            else:
                raise TypeError("Variable: {} hasnt been declared. At line {}".format(name, lineno))
        else:
            if name in self.diccionario['dirFunc']['global']['vars'].keys():
                return self.diccionario['dirFunc']['global']['vars'][name]
            elif name in self.diccionario['dirFunc'][scope]['vars'].keys():
                return self.diccionario['dirFunc'][scope]['vars'][name]
            #elif (scope != 'global' and scope != 'main'):
                #if aux_dato in self.diccionario['dirFunc'][scope]['params'].keys():
                #return self.diccionario['dirFunc'][scope]['params'][aux_dato]
            else:
                raise TypeError("Variable: {} hasnt been declared. At line {}".format(name, lineno))

    def get_constantinfo(self, name, type, lineno):
        if name in self.diccionario['dirFunc']['constantes']['vars'].keys():
            return self.diccionario['dirFunc']['constantes']['vars'][name]
        else:
            return self.insert_constant(name,type)


    def insert_constant(self, name, type):
        direccion = self.contador['contador']['constantes'][type]
        self.contador['contador']['constantes'][type] += 1
        new_constant = {
            'name': name,
            'type': type,
            'direccion': direccion
        }
        self.diccionario['dirFunc']['constantes']['vars'][name] = new_constant
        return new_constant

    def get_funcinfo(self, scope, aux_parameter):
        if scope in self.diccionario['dirFunc'].keys():
            aux_parameter.name = scope
            aux_parameter.type = self.diccionario['dirFunc'][scope]['type']
            aux_parameter.params = dict(self.diccionario['dirFunc'][scope]['params'])
            aux_parameter.length = len(aux_parameter.params)
        else:
            raise TypeError("Funtion: {} hasnt been declared".format(aux_dato))

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
