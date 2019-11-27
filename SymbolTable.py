import sys
from Contador import Contador

globalinicio = 10000
constanteinicio = 20000
localinicio = 30000

class SymbolTable:
    def __init__(self):
        self.diccionario ={'dirFunc':{}}
        self.contador = {'contador':{}}

    def create_table_globalcons(self, name):
        if(name=='global'):
            inicio = globalinicio
        elif(name == 'constantes'):
            inicio = constanteinicio

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

    def create_table_function(self, tabla, lineno):
        self.lookup_function(tabla.name, lineno)
        inicio = localinicio
        new_table = {
            'name': tabla.name,
            'type' : tabla.type,
            'inicio' : tabla.posicion_inical,
            'params' : {},
            'vars' : {},
            'return' : None
        }
        self.diccionario['dirFunc'][tabla.name] = new_table

        new_contador = {
            'name' : tabla.name,
            'inicio': inicio,
            'limite' : 999,
            'int' : inicio,
            'float' : inicio + 1000,
            'string' : inicio + 2000,
            'bool' : inicio + 3000,
        }
        self.contador['contador'][tabla.name] = new_contador

        if(tabla.type != "void"):
            self.insert_function_as_global(tabla, lineno)


    def lookup_function(self, name, lineno):
        if name in self.diccionario['dirFunc'].keys():
            raise TypeError("Function: {} already exists. At line: {}".format(tabla.name, lineno))
        if name in self.diccionario['dirFunc']['global']['vars'].keys():
            raise TypeError("Function: {} already declared as global variable. At line: {}".format(tabla.name, lineno))

    def create_table_main(self):
        name = "main"
        inicio = localinicio
        new_table = {
            'name': "main",
            'inicio' : 0,
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

    def insert_function_as_global(self, tabla, lineno):
        direccion = self.create_direccion_simplified(tabla.type, 'global')
        new_variable = {
            'name': tabla.name,
            'type': tabla.type,
            'cons' : False,
            'complex': "simple",
            'direccion': direccion
        }
        self.diccionario['dirFunc']['global']['vars'][tabla.name] = new_variable

    def insert_variable(self, dato, tabla, lineno):
        scope = tabla.name
        self.lookup_variable(dato.name, scope, lineno)
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

        if(dato.parameter):
            self.diccionario['dirFunc'][scope]['params'][dato.name] = new_variable
        else:
            self.diccionario['dirFunc'][scope]['vars'][dato.name] = new_variable

    def lookup_variable(self, dato, scope, lineno):
        if (scope == 'global'):
            if dato in self.diccionario['dirFunc']['global']['vars'].keys():
                raise TypeError("Variable: {} already declared as global. At line: {}".format(dato, lineno))
        else:
            if dato in self.diccionario['dirFunc'][scope]['vars'].keys():
                raise TypeError("Variable: {} already declared in same scope ({}). At line {}".format(dato, scope, lineno))
            elif dato in self.diccionario['dirFunc']['global']['vars'].keys():
                raise TypeError("Variable: {} already declared as global. At line: {}".format(dato, lineno))
            elif (scope != 'global' and scope != 'main'):
                if dato in self.diccionario['dirFunc'][scope]['vars'].keys():
                    raise TypeError("Variable: {} already declared as parameter. At line: {}".format(dato, lineno))

    def create_direccion_simplified(self, type, scope):
        direccion = self.contador['contador'][scope][type]
        self.contador['contador'][scope][type] += 1
        return direccion

    def create_direccion(self, dato, scope):
        direccion = self.contador['contador'][scope][dato.type]
        if(dato.complex == "simple"):
            self.contador['contador'][scope][dato.type] += 1
        else:
            self.contador['contador'][scope][dato.type] += dato.tamano
        return direccion

    def create_complex_limits(self, dato):
        if (dato.complex == "arr"):
            tamano = dato.tamano[0] + 1
            return tamano, {'limite1' : dato.tamano[0]}
        elif (dato.complex == "mat"):
            limite1 = dato.tamano[0]
            limite2 = dato.tamano[1]
            tamano = (limite1 + 1) * (limite2 + 1)
            m1 = int(tamano / (limite1 + 1))
            return tamano, {'limite1' : limite1, 'limite2' : limite2, 'm1' : m1}

    def get_variable(self, name, scope, lineno):
        if (scope == 'global' or scope =='return'):
            if name in self.diccionario['dirFunc']['global']['vars'].keys():
                return self.diccionario['dirFunc']['global']['vars'][name]
            else:
                if(scope == 'global'):
                    raise TypeError("Variable: {} hasnt been declared. At line {}".format(name, lineno))
                else:
                    raise TypeError("Void Function: {} cant return. At line {}".format(name, lineno))
        else:
            if name in self.diccionario['dirFunc']['global']['vars'].keys():
                return self.diccionario['dirFunc']['global']['vars'][name]
            elif name in self.diccionario['dirFunc'][scope]['vars'].keys():
                return self.diccionario['dirFunc'][scope]['vars'][name]
            elif (scope != 'global' and scope != 'main'):
                if name in self.diccionario['dirFunc'][scope]['params'].keys():
                    return self.diccionario['dirFunc'][scope]['params'][name]
            else:
                raise TypeError("Variable: {} hasnt been declared. At line {}".format(name, lineno))

    def get_constant(self, name, type, lineno):
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
            'direccion': direccion,
            'complex' : "simple"
        }
        self.diccionario['dirFunc']['constantes']['vars'][name] = new_constant
        return new_constant

    def get_function_info(self, scope, aux_parameter, lineno):
        if scope in self.diccionario['dirFunc'].keys():
            aux_parameter.name = scope
            aux_parameter.type = self.diccionario['dirFunc'][scope]['type']
            aux_parameter.params = dict(self.diccionario['dirFunc'][scope]['params'])
            aux_parameter.length = len(aux_parameter.params)
        else:
            raise TypeError("Function: {} hasnt been declared. At Line: {}".format(scope, lineno))

    def validdt(self, tipo):
        switch = {
            'int' : True,
            'string' : True,
            'float' : True,
            'bool' : True,
        }
        if not (switch.get(tipo, False)):
            raise TypeError("Variable Type: {} not valid.".format(tipo))

    def get_constant_table(self):
        tabla_constantes_aux = {}
        for key in self.diccionario['dirFunc']['constantes']['vars']:
            test = self.diccionario['dirFunc']['constantes']['vars'][key]
            tabla_constantes_aux[test['direccion']] = test['name']
        self.diccionario['dirFunc']['constantes'] = dict(tabla_constantes_aux)

#Cementerio de funciones

    def lookup_variablefunc(self, dato, scope):
        if dato.id in self.diccionario['dirFunc']['global']['vars'].keys():
            raise TypeError("Variable: {} already declared as global".format(dato.id))
        if dato.id in self.diccionario['dirFunc']['global']['cons'].keys():
            raise TypeError("Variable: {} already declared as global".format(dato.id))
        if dato.id in self.diccionario['dirFunc'][scope]['params'].keys():
            raise TypeError("Variable: {} already declared as parameter".format(dato.id))
