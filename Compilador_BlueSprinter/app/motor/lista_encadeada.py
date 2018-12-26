class No(object):
    def __init__(self, conteudo):
        super(No, self).__init__()
        self.conteudo = conteudo
        self.proximo = None


class ListaEncadeada(object):
    def __init__(self):
        super(ListaEncadeada, self).__init__()
        self.raiz = None
        self.__length = 0

    def insere(self, conteudo):
        novoNo = No(conteudo)
        if self.raiz is None:
            self.raiz = novoNo
        else:
            novoNo.proximo = self.raiz
            self.raiz = novoNo
        self.__length += 1

    def insere_no_fim(self, conteudo):
        novoNo = No(conteudo)
        if self.raiz is not None:
            noAtual = self.raiz
            while noAtual.proximo is not None:
                noAtual = noAtual.proximo
            noAtual.proximo = novoNo
        else:
            self.raiz = novoNo
        self.__length += 1

    def remove(self):
        if self.raiz is not None:
            if self.raiz.proximo is not None:
                noAtual = self.raiz
                # busca o penúltimo No
                while noAtual.proximo.proximo is not None:
                    noAtual = noAtual.proximo
                # retira o último No
                noRet = noAtual.proximo
                noAtual.proximo = None
            else:
                noRet = self.raiz
                self.raiz = None
            self.__length -= 1
            return noRet.conteudo
        else:
            return None
    
    def imprimir(self):
        atual = self.raiz
        while atual:
            print(atual.conteudo)
            atual = atual.proximo
        print()

    def __len__(self):
        return self.__length

    def __bool__(self):
        return self.__length != 0
