from . import TransdutorFinito


class Submaquina(TransdutorFinito):
    def __init__(self, nome, **kwargs):
        super(Submaquina, self).__init__(nome, **kwargs)

    def tem_transicao_para_submaquina(self):
        return bool(self._estadoAtual.submaquinas_chamadas)

    def add_chamada_para_submaquina(self, de, para, retorno):
        self.add_estado(de)
        self.add_estado(retorno)
        self[de].add_chamada_para_submaquina(para, self[retorno])

    def get_parametros_de_chamada(self):
        if self.tem_transicao_para_submaquina():
            prox_maq = list(self._estadoAtual.submaquinas_chamadas)[0]
            if (self._estadoAtual.nome, prox_maq) in self.saidas:
                self.saida_gerada = self.saidas[(self._estadoAtual.nome, prox_maq)]
            else:
                self.saida_gerada = None
            return prox_maq, self._estadoAtual[prox_maq]
        else:
            return (None, None)


class AutomatoPilhaEstruturado:
    """implementa um Autômato de Pilha Estruturado"""
    def __init__(self, nome, **kwargs):
        super(AutomatoPilhaEstruturado, self).__init__()
        # nome do autômato
        self.nome = nome
        # sub-máquinas
        if 'sub_maquinas' in kwargs and kwargs['sub_maquinas'] is not None:
            self.__automatos = {
                submaq: Submaquina(nome=submaq) for submaq in kwargs['sub_maquinas']
            }
            if 'automatoInicial' in kwargs and kwargs['automatoInicial'] is not None:
                self.__maquinaInicial = kwargs['automatoInicial']
        else:
            self.__automatos = {}
        # configuração
        self.__maquinaAtual = None
        # Pilha
        self.__pilha = []

        # alfabeto
        self.alfabeto = set()
        self.__simboloAtual = None

    def add_submaquina(self, nome, estados, estadoInicial, estadosFinais, alfabeto):
        if nome not in self.__automatos:
            self.__automatos[nome] = Submaquina(nome=nome, estados=estados, estadoInicial=estadoInicial, estadosFinais=estadosFinais, alfabeto=alfabeto)

    def gerar_alfabeto(self):
        for S in self.__automatos.values():
            self.alfabeto.update(S.alfabeto)

    def set_submaquina_inicial(self, sub_maq):
        self.__maquinaInicial = self.__automatos[sub_maq]

    def inicializar(self):
        """põe o Automato de Pilha Estruturado no estado inicial e dá outras providências."""
        self.__maquinaAtual = self.__maquinaInicial
        self.__maquinaAtual.inicializar()

    def atualizar_simbolo(self, simbolo):
        if simbolo in self.alfabeto:
            self.__simboloAtual = simbolo
        else:
            raise ValueError("Erro ao atualizar símbolo: '{}' não pertence ao alfabeto".format(simbolo))
        self.__maquinaAtual.atualizar_simbolo(simbolo)

    def fazer_transicao(self):
        # tenta fazer uma transição dentro da sub-máquina atual
        transitou = self.__maquinaAtual.fazer_transicao()
        self.__saida_gerada = self.__maquinaAtual.saida_gerada
        return transitou

    def chama(self):
        # Pega a próxima sub-máquina e o estado de retorno
        proxMaquina, estadoRetorno = self.__maquinaAtual.get_parametros_de_chamada()
        self.__saida_gerada = self.__maquinaAtual.saida_gerada
        # Empilha a sub-máquina de retorno e o estado de retorno
        self.__pilha.append((self.__maquinaAtual, estadoRetorno))
        # Troca de sub-máquina e a inicializa
        self.__maquinaAtual = self[proxMaquina]
        self.__maquinaAtual.inicializar()

    def retorna(self):
        if self.__pilha:
            submaqRet, estadoRetorno = self.__pilha.pop()
            estadoAtual, _ = self.__maquinaAtual.mConfiguracao()
            if (estadoAtual.nome, 'pop') in self.__maquinaAtual.saidas:
                self.__saida_gerada = self.__maquinaAtual.saidas[(estadoAtual.nome, 'pop')]
            else:
                self.__saida_gerada = None
            self.__maquinaAtual = submaqRet
            self.__maquinaAtual.inicializar(estadoRetorno)

    def mConfiguracao(self):
        return self.__maquinaAtual.mConfiguracao()

    @property
    def saida_gerada(self):
        return self.__saida_gerada

    @property
    def sub_maquina_atual(self):
        return self.__maquinaAtual

    def __getitem__(self, sub_maq):
        if sub_maq in self.__automatos:
            return self.__automatos[sub_maq]
        else:
            return None

    def tem_retorno_a_realizar(self):
        return bool(self.__pilha)
