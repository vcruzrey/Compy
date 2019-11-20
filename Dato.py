class Dato:
    def __init__(self):
        self.scope =''
        self.name = ''
        self.id =''
        self.complex = 'simple'
        self.cons = False
        self.type = ''
        self.parameter = False

    def reset(self):
        self.scope =''
        self.name = ''
        self.id =''
        self.complex = 'simple'
        self.cons = False
        self.type = ''
        self.parameter = False

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
