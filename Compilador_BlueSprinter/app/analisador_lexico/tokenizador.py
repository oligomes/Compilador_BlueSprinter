import string
from ..motor import MotorEventos, Evento


class AnalisadorLexico(MotorEventos):
    def __init__(self, automato, palavras_reservadas=()):
        super(AnalisadorLexico, self).__init__()
        self.__palavras_reservadas = palavras_reservadas
        self._automato = automato
        self.__classificacoes = {}
        self.add_evento(Evento('PartidaInicial'))


    def trata_evento(self, evento):
        if evento.tipo == 'PartidaInicial':
            self.PartidaInicial()
        elif evento.tipo == 'ReiniciarAutomato':
            self.ReiniciarAutomato()
        elif evento.tipo == 'ChegadaSimbolo':
            self.ChegadaSimbolo(evento.informacao)
        elif evento.tipo == 'CursorParaDireita':
            self.CursorParaDireita()
        elif evento.tipo == 'ExecutarTransducao':
            self.ExecutarTransducao()
        elif evento.tipo == 'LeituraSimbolo':
            self.LeituraSimbolo()


    def PartidaInicial(self):
        # poe o automato no estado inicial
        self._automato.inicializar()
        # põe os dados na "fita"
        self.__fita = ['']
        self.__cursor = 0
        self.token_atual = ''
        self.valor_token = 0 # Para numerais
        self.tokens = []


    def ReiniciarAutomato(self):
        if self._automato._estadoAtual.final:
            self.categorizar()
        # Põe o autômato no estado inicial
        self._automato.inicializar()
        self.token_atual = ''
        self.valor_token = 0
        self.add_evento(Evento('LeituraSimbolo'), no_fim=True)


    def ChegadaSimbolo(self, c):
        self.__fita[self.__cursor] = c
        self.add_evento(Evento('LeituraSimbolo'), no_fim=True)


    def LeituraSimbolo(self):
        c = self.__fita[self.__cursor]
        try:
            self._automato.atualizar_simbolo(c[1])
            transitou = self._automato.fazer_transicao()
        except Exception as e:
            print(e)
            transitou = False

        if transitou:
            self.token_atual += c[0]
            if self._automato.saida_gerada is not None:
                self.add_evento(Evento('ExecutarTransducao'), no_fim=True)
            self.add_evento(Evento('CursorParaDireita'), no_fim=True)
        else:
            self.add_evento(Evento('ReiniciarAutomato'), no_fim=True)


    def CursorParaDireita(self):
        self.__fita.append('')
        self.__cursor += 1


    def ExecutarTransducao(self):
        rotina = self._automato.saida_gerada
        if rotina == 'aspas':
            self.aspas()
        elif rotina == 'limpa':
            self.limpa()
        elif rotina == 'numeroDecimal':
            self.numeroDecimal()


    def add_classificacao(self, estado_final, classificacao):
        self.__classificacoes[estado_final] = classificacao


    def categorizar(self):
        # por default, o tipo do token é igual a ele mesmo
        token_tipo = self.token_atual
        for estado_final, classificacao in self.__classificacoes.items():
            # até que se prove o contrário
            if self._automato._estadoAtual == estado_final:
                token_tipo = classificacao
        self.tokens.append((self.token_atual, token_tipo))
        self.pos_categorizar()


    def pos_categorizar(self):
        token_atual, token_tipo = self.tokens[-1]

        if (token_tipo == "NumeroDecimal"
           or token_tipo == "NumeroHexadecimal"):
                self.tokens[-1] = (self.valor_token, "Numero")
        elif token_tipo == "Identificador":
            if token_atual in self.__palavras_reservadas:
                self.tokens[-1] = (token_atual, token_atual)


    def aspas(self):
        self.token_atual += '"'


    def limpa(self):
        self.token_atual = self.token_atual[:-1]


    def numeroDecimal(self):
        self.valor_token *= 10
        self.valor_token += int(self.token_atual[-1])
