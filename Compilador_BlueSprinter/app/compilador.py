import os
import app.automatos.loaders as loaders
from .analisador_lexico.extrator_linhas import ExtratorLinhas
from .analisador_sintatico.analisador_sintatico import AnalisadorSintatico
from .analisador_semantico.analisador_semantico import AnalisadorSemantico
from .motor import Evento
from .conf import ROOT_DIR


class Compilador:
    def __init__(self):
        self.extrator = ExtratorLinhas()
        automato_sintatico = loaders.automato_pilha_estruturado(os.path.join(ROOT_DIR, 'app', 'analisador_sintatico', 'bluesprinter.ap'))
        self.analisador_semantico = AnalisadorSemantico()
        self.analisador_sintatico = AnalisadorSintatico(automato_sintatico, self.analisador_semantico)


    def compilar(self, nome_arquivo):
        self.extrator.add_evento(Evento('AbrirArquivo', nome_arquivo))
        self.extrator.run()

        self.analisador_sintatico.add_evento(Evento('PartidaInicial'))
        for tok in self.extrator.filtro.tokenizer.tokens:
            self.analisador_sintatico.add_evento(Evento('ChegadaSimbolo', tok))
        self.analisador_sintatico.run()


    def exportar(self, arquivo_saida):
        with open(arquivo_saida, 'w') as f:
            for line in self.analisador_semantico.preambulo:
                f.write(line + '\n')
            f.write('; declaracao de CONSTANTES\n')
            for line in self.analisador_semantico.constantes:
                f.write(line + '\n')
            f.write('; declaracao de FUNCOES\n')
            for line in self.analisador_semantico.codigo:
                f.write(line + '\n')
            f.write('# FIM\n')
 