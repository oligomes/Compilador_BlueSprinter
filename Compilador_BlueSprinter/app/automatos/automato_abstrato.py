from .estado import Estado


class AutomatoAbstrato:
    def __init__(self, deterministico=True):
        super(AutomatoAbstrato, self).__init__()
        self.alfabeto = set()
        self.estados = {}
        self.deterministico = deterministico

    def add_estado(self, nome_estado, final=False):
        if nome_estado not in self.estados:
            self.estados[nome_estado] = Estado.factory(nome_estado, final, self.deterministico)

    def add_transicao(self, de, com, para):
        self.add_estado(de)
        self.add_estado(para)
        self.estados[de][com] = self.estados[para]
        if com != '':
            self.gerar_alfabeto()

    def gerar_alfabeto(self):
        for q in self:
            for s in q.simbolos:
                if s != '':
                    self.alfabeto.add(s)
        for q in self:
            for s in self.alfabeto:
                if self.deterministico and s not in q.simbolos:
                    q[s] = None

    @property
    def alfabeto_sem_chamada_de_submaquina(self):
        chamadas = set()
        for q in self:
            chamadas |= q.submaquinas_chamadas
        return self.alfabeto.difference(chamadas)

    def __getitem__(self, nome_estado):
        if nome_estado in self.estados:
            return self.estados[nome_estado]
        else:
            return None

    def __iter__(self):
        for el in self.estados.values():
            yield el
