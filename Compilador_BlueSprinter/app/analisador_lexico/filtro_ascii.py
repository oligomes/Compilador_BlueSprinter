import os
import string
import app.automatos.loaders as loaders
from ..motor import MotorEventos, Evento
from .tokenizador import AnalisadorLexico
from ..conf import ROOT_DIR


class Filtro(MotorEventos):
    def __init__(self):
        super(Filtro, self).__init__()
        self.categorias = { 'controle':['\n'],
                            'delimitador':['\t', ' '],
                            'letra': string.ascii_uppercase[6:] + string.ascii_lowercase[6:],
                            'zero': string.digits[0],
                            'digito_dec': string.digits[1:],
                            'digito_hex': string.ascii_uppercase[:6] + string.ascii_lowercase[:6]}
        self.categorias.update({s: s for s in string.punctuation})
        self.caracteres_classificados = []
        self.automato_tokenizador = loaders.transdutor_finito(os.path.join(ROOT_DIR, 'app', 'automatos', 'tokenizer.af'))
        self.tokenizer = AnalisadorLexico(self.automato_tokenizador, palavras_reservadas=['var', 'par', 'int', 'char', 'bool', 'True', 'False', 'or', 'and', 'not', 'return', 'if', 'elif', 'else', 'while', 'def', 'len'])
        self.tokenizer.add_classificacao('q39', 'enter')
        self.tokenizer.add_classificacao('q15', 'Identificador')
        self.tokenizer.add_classificacao('q29', 'NumeroDecimal')
        self.tokenizer.add_classificacao('q30', 'NumeroDecimal')
        self.tokenizer.add_classificacao('q4', 'Comparacao')  # ==
        self.tokenizer.add_classificacao('q7', 'Comparacao')  # >=
        self.tokenizer.add_classificacao('q20', 'Comparacao') # <=
        self.tokenizer.add_classificacao('q27', 'Comparacao') # !=
        self.tokenizer.add_classificacao('q36', 'Comparacao') # >
        self.tokenizer.add_classificacao('q22', 'Comparacao') # <

    def trata_evento(self, evento):
        if evento.tipo == 'LeituraCaractere':
            self.leitura_caractere(*evento.informacao)
        elif evento.tipo == 'ChegadaLinha':
            self.chegada_linha(*evento.informacao)

    def leitura_caractere(self, caractere, num):
        for categoria, conjunto in self.categorias.items():
            if caractere in conjunto:
                classificacao = categoria
        self.caracteres_classificados.append((caractere, classificacao))
        self.tokenizer.add_evento(Evento('ChegadaSimbolo', (caractere, classificacao)))
        self.tokenizer.run()

    def chegada_linha(self, linha, num):
        for i in range(len(linha)):
            caractere = linha[i]
            self.add_evento(Evento('LeituraCaractere', (caractere,i)))
