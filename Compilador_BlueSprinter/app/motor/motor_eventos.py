from .lista_encadeada import ListaEncadeada


class MotorEventos:
    def __init__(self):
        self._listaEventos = ListaEncadeada()

    def trata_evento(self, evento):
        pass

    def add_evento(self, evento, no_fim=False):
        if no_fim:
            self._listaEventos.insere_no_fim(evento)
        else:
            self._listaEventos.insere(evento)

    def run(self):
        evento_final = False
        while self._listaEventos and not evento_final:
            proximo_evento = self._listaEventos.remove()
            evento_final = proximo_evento.final
            self.trata_evento(proximo_evento)
