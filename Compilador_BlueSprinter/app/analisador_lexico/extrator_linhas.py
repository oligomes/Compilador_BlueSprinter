import string
from ..motor import MotorEventos, Evento
from .filtro_ascii import Filtro


class ExtratorLinhas(MotorEventos):
    def __init__(self):
        super(ExtratorLinhas, self).__init__()
        self.linhas_indexadas = []
        self.filtro = Filtro()

    def trata_evento(self, evento):
        if evento.tipo == 'AbrirArquivo':
            self.abrir_arquivo(evento.informacao)
        elif evento.tipo == 'FecharArquivo':
            self.fechar_arquivo()
        elif evento.tipo == 'LeituraLinha':
            self.leitura_linha()
        elif evento.tipo == 'IOError':
            self.erro_leitura(evento.informacao)

    def abrir_arquivo(self, nome_arquivo):
        self.contador_linhas = 0
        try:
            self.arquivo_fonte = open(nome_arquivo)
            self.add_evento(Evento('LeituraLinha'))
        except:
            self.add_evento(Evento('IOError', "Não foi possível abrir '{}': arquivo não encontrado.".format(nome_arquivo)))

    def fechar_arquivo(self):
        self.arquivo_fonte.close()

    def leitura_linha(self):
        linha = self.arquivo_fonte.readline()
        if linha:
            self.filtro.add_evento(Evento('ChegadaLinha', (linha, self.contador_linhas)))
            self.filtro.run()
            self.add_evento(Evento('LeituraLinha'))
            self.contador_linhas += 1
        else:
            self.add_evento(Evento('FecharArquivo'))

    def erro_leitura(self, msg):
        print(msg)
