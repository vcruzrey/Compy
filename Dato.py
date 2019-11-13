class Dato:
    def __init__(self):
        self.scope =''
        self.name = ''
        self.id =''
        self.array = False

        self.cons = False
        self.type = ''

    def reset(self):
        self.type = ''
        self.scope =''
        self.name = ''
        self.id =''
        self.array = False
        self.cons = False
