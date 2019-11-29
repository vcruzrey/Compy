class Dato:
    def __init__(self):
        self.scope =''
        self.name = ''
        self.complex = 'simple'
        self.cons = False
        self.type = ''
        self.parameter = False
        self.tamano = []

    def reset(self):
        self.scope =''
        self.name = ''
        self.complex = 'simple'
        self.cons = False
        self.type = ''
        self.parameter = False
        self.tamano = []

class Parameter:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.params = {}
        self.length = 0
        self.contador = 0

    def reset(self):
        self.name = ''
        self.type = ''
        self.params = {}
        self.length = 0
        self.contador = 0

class SpecialFunc:
    def __init__(self):
        self.name = ''

    def reset(self):
        self.name = ''
