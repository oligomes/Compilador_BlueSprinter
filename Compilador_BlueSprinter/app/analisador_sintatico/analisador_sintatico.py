from ..motor import MotorEventos, Evento


class AnalisadorSintatico(MotorEventos):
    def __init__(self, automato, gerador_codigo):
        super(AnalisadorSintatico, self).__init__()
        self.ap = automato
        self.__gerador_codigo = gerador_codigo

    def trata_evento(self, evento):
        if evento.tipo == 'PartidaInicial':
            self.PartidaInicial()
        elif evento.tipo == 'CursorParaDireita':
            self.CursorParaDireita()
        elif evento.tipo == 'LeituraSimbolo':
            self.LeituraSimbolo()
        elif evento.tipo == 'ChegadaSimbolo':
            self.ChegadaSimbolo(evento.informacao)
        elif evento.tipo == 'ChamadaSubmaquina':
            self.ChamadaSubmaquina()
        elif evento.tipo == 'RetornoSubmaquina':
            self.RetornoSubmaquina()
        elif evento.tipo == 'ExecutarTransducao':
            self.ExecutarTransducao(evento.informacao)
        elif evento.tipo == 'FimEntrada':
            self.FimEntrada()
        elif evento.tipo == 'Erro':
            self.Erro()

    def PartidaInicial(self):
        self.ap.inicializar()
        self.__fita = ['']
        self.__cursor = 0

    def ChegadaSimbolo(self, simbolo):
        self.__fita[self.__cursor] = simbolo
        self.add_evento(Evento('LeituraSimbolo'), no_fim=True)

    def CursorParaDireita(self):
        self.__fita.append('')
        self.__cursor += 1

    def ChamadaSubmaquina(self):
        self.ap.chama()
        if self.ap.saida_gerada is not None:
            self.add_evento(Evento('ExecutarTransducao'), no_fim=True)

    def RetornoSubmaquina(self):
        self.ap.retorna()
        if self.ap.saida_gerada is not None:
            self.add_evento(Evento('ExecutarTransducao'), no_fim=True)

    def LeituraSimbolo(self):
        simbolo = self.__fita[self.__cursor]
        val, tok = simbolo
        try:
            self.ap.atualizar_simbolo(tok)
            transitou = self.ap.fazer_transicao()
        except:
            transitou = False

        if not transitou:
            estado_atual, _ = self.ap.mConfiguracao()
            # tentar fazer chamda de sub-maquina
            if self.ap.sub_maquina_atual.tem_transicao_para_submaquina():
                self.add_evento(Evento('LeituraSimbolo'), no_fim=True)
                self.add_evento(Evento('ChamadaSubmaquina'), no_fim=True)
            # senao, tenta voltar a uma suposta maquina anterior
            elif estado_atual.final and self.ap.tem_retorno_a_realizar():
                self.add_evento(Evento('LeituraSimbolo'), no_fim=True)
                self.add_evento(Evento('RetornoSubmaquina'), no_fim=True)
            # se nenhuma das duas opcoes deu ceerto, entao emite um sinal de erro
            else:
                self.add_evento(Evento('Erro', final=True), no_fim=True)
        else:
            self.add_evento(Evento('CursorParaDireita'), no_fim=True)
            if self.ap.saida_gerada is not None:
                self.add_evento(Evento('ExecutarTransducao', val), no_fim=True)

    def ExecutarTransducao(self, token):
        rotina = self.ap.saida_gerada
        self.__gerador_codigo(rotina, token)

    def FimEntrada(self):
        estado_atual, _ = self.ap.mConfiguracao()
        if not self.ap.tem_retorno_a_realizar() and estado_atual.final:
            print('resultado: CADEIA ACEITA')
        else:
            print('resultado: CADEIA REJEITADA')

    def Erro(self):
        print('Erro')
        print('Sub-máquina atual:', self.ap.sub_maquina_atual.nome)
        print('Estado: {0[0]}\nSimbolo: {0[1]}'.format(self.ap.mConfiguracao()))
        print('resultado: CADEIA REJEITADA')
