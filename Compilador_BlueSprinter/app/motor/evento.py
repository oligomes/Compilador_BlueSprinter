class Evento:
    def __init__(self, tipo, informacao='', final=False):
        self.tipo = tipo
        self.informacao = informacao
        self.final = final

    def __str__(self):
        return "({}, {})".format(self.tipo, self.informacao)
