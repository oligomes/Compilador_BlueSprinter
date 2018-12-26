class Simbolo:
	def __init__(self, nome, especie, tipo):
		self.nome = nome
		self.tipo = tipo
		self.especie = especie
		self.posicao = None
		self.referenciado = False
		self.utilizado = False
	def __repr__(self):
		return self.nome


class SimboloConst(Simbolo):
	def __init__(self, nome, especie, tipo, valor):
		super(SimboloConst, self).__init__(nome, especie, tipo)
		self.valor = valor


class SimboloFunc(Simbolo):
	def __init__(self, nome, tipo):
		super(SimboloFunc, self).__init__(nome, "func", tipo)
		self.offset_end_retorno = -2 # End. Ret. == F[-1]
		self.offset_fp_old = 0 # FP_OLD == FP[0]
		self.pilha_parametros_offset = -4 # Parâmetros começam apenas em FP[-2] para baixo
		self.pilha_variaveis_offset = 0 # esse valor será atualizado a cada variável recebida
		self.offset_valor_retorno = 0 # esse valor depende da quantidade de parâmetros
		self.variaveis = {}
		self.parametros = {}

	def add_parametro(self, simb):
		i = len(self.parametros)
		self.parametros[i] = simb

	def add_variavel(self, simb):
		i = len(self.variaveis)
		self.variaveis[i] = simb


class SimboloArray(Simbolo):
	def __init__(self, nome, especie, tipo, dimensoes=[]):
		super(SimboloArray, self).__init__(nome, especie, tipo)
		self.dimensoes = list(dimensoes)
		self.cursor_atual = 0


class TipoBasico:
	def __init__(self, s, tamanho):
		super(TipoBasico, self).__init__()
		self.s = s
		self.tamanho = tamanho

	def __eq__(self, s):
		return s == self.s


class TabelaSimbolos:

	class Escopo:
		def __init__(self, pai):
			super(TabelaSimbolos.Escopo, self).__init__()
			self.pai = pai
			self.simbolos = []

		def __getitem__(self, k):
			return self.simbolos[k]

	def __init__(self):
			super(TabelaSimbolos, self).__init__()
			self.escopo_global= TabelaSimbolos.Escopo(pai=None)
			self.escopo_atual = self.escopo_global

	def novo_escopo(self):
		escopo = TabelaSimbolos.Escopo(pai=self.escopo_atual)
		self.escopo_atual = escopo

	def remover_escopo(self):
		if self.escopo_atual.pai is not None:
		    self.escopo_atual = self.escopo_atual.pai

	def inserir_simbolo(self, simbolo):
		self.escopo_atual.simbolos.append(simbolo)

	def procurar(self, simbolo):
		p = self.escopo_atual
		while p is not None:
			for s in range(len(p.simbolos)):
				if p.simbolos[s].nome == simbolo:
					return p[s]
			p = p.pai
		return None

	def existe(self, label):
		for simbolo in self.escopo_global.simbolos:
			if simbolo.nome == label:
				return True
		return False

	def procurar_localmente(self, label):
		for simbolo in self.escopo_atual.simbolos:
			if simbolo.nome == label:
				return simbolo
		return None

	def inserir_const(self, simbolo):
		self.escopo_global.simbolos.append(simbolo)

