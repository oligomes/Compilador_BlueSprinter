class Estado:
    """representa um Estado com suas transições"""
    def __init__(self, nome, final=False):
        super(Estado, self).__init__()
        self.nome = nome
        self.final = final
        self.transicoes = {}
        self.submaquinas_chamadas = set()

    @staticmethod
    def factory(nome, final=False, deterministico=True):
        if deterministico:
            return EstadoDeterministico(nome, final)
        else:
            return EstadoNaoDeterministico(nome, final)

    @property
    def simbolos(self):
        return set(self.transicoes.keys())

    def __delitem__(self, simbolo):
        if simbolo in self.transicoes:
            del self.transicoes[simbolo]

    def add_chamada_para_submaquina(self, para, retorno):
        self.submaquinas_chamadas.add(para)
        self.__setitem__(para, retorno)

    def __getitem__(self, simbolo):
        return self.transicoes[simbolo]

    def __eq__(self, estado):
        if isinstance(estado, Estado):
            return self == estado.nome
        else:
            return self.nome == estado

    def __str__(self):
        return self.nome

    def __repr__(self):
        return self.nome


class EstadoDeterministico(Estado):
    def __init__(self, nome, final=False):
        super(EstadoDeterministico, self).__init__(nome, final)

    def __setitem__(self, simbolo, prox):
            self.transicoes[simbolo] = prox


class EstadoNaoDeterministico(Estado):
    def __init__(self, nome, final=False):
        super(EstadoNaoDeterministico, self).__init__(nome, final)

    def merge(self, Sj, com_transicoes_em_vazio=False):
        for simbolo in Sj.transicoes.keys():
            if (com_transicoes_em_vazio or
               (not com_transicoes_em_vazio and simbolo != '')):
                    if simbolo in self.transicoes:
                        for estado_destinho in Sj[simbolo]:
                            if estado_destinho not in self.transicoes[simbolo]:
                                self.transicoes[simbolo].append(estado_destinho)
                    else:
                        if simbolo in Sj.transicoes:
                            self.transicoes[simbolo] = list(Sj[simbolo])
        self.final |= Sj.final
        self.submaquinas_chamadas |= Sj.submaquinas_chamadas

    def __setitem__(self, simbolo, prox):
        if simbolo not in self.transicoes:
            self.transicoes[simbolo] = [prox]
        elif prox not in self.transicoes[simbolo]:
            self.transicoes[simbolo].append(prox)
