import re
from .automato_finito import TransdutorFinito
from .automato_pilha_estruturado import AutomatoPilhaEstruturado


__all__ = ['transdutor_finito']


def parse_tf(espec):
    match_automato = re.compile(r'^[\s\t]*<(?P<nome>\w+)>\n(.*)\s*</(?P=nome)>', re.DOTALL | re.MULTILINE)
    match_transicoes = re.compile(r"\(([a-zA-Z]\w*)\s*,\s*'(.+)'\s*\)\s*->\s*([a-zA-Z]\w*)(?:\s*\\\s*(\w+))?\n")

    match_output_1 = match_automato.search(espec)
    nome_automato = match_output_1.group(1)
    linhas = match_output_1.group(2).split('\n')

    # estados
    estados = re.sub(r'^[\s\t]+', r'', linhas[0]).split()

    # inicial
    inicial = re.sub(r'^[\s\t]+', r'', linhas[1])

    # estados finais
    finais = re.sub(r'^[\s\t]+', r'', linhas[2]).split()

    # alfabeto
    alfabeto = re.sub(r'^[\s\t]+', r'', linhas[3]).split()

    # Automato Transdutor
    tf = TransdutorFinito(nome=nome_automato, estados=estados, estadoInicial=inicial, estadosFinais=finais, alfabeto=alfabeto)

    for match_output_2 in match_transicoes.finditer(match_output_1.group(2)):
        qi, s, qj, saida = match_output_2.groups()
        tf.add_transicao(de=qi, com=s, para=qj)
        if saida is not None:
            tf.add_saida(de=qi, com=s, saida=saida)

    return tf


def transdutor_finito(nome_arquivo):
    with open(nome_arquivo) as f:
        texto = f.read()
        texto = re.sub(r'\n+', '\n', texto)
        return parse_tf(texto)

    return None


def automato_pilha_estruturado(nome_arquivo):
    with open(nome_arquivo) as f:
        texto = f.read()
        texto = re.sub(r'\n+', '\n', texto)

        match_automato = re.compile(r'[\s\t]*<(?P<nome>\w+)>\n(.*)</(?P=nome)>', re.DOTALL | re.MULTILINE)

        mo1 = match_automato.search(texto)
        nome_automato = mo1.group(1)
        linhas = mo1.group(2).split('\n')[:2]

        maquinas = re.sub(r'^[\s\t]+', r'', linhas[0]).split()
        maquina_inicial = re.sub(r'^[\s\t]+', r'', linhas[1])

        ape = AutomatoPilhaEstruturado(nome=nome_automato)

        match_transicoes = re.compile(r"\(([a-zA-Z]\w*)\s*,\s*'(.+)'\s*\)\s*->\s*([a-zA-Z]\w*)(?:\s*\\\s*([\(\)\[\]\{\}|\w]+))?\n")
        match_chamadas = re.compile(r"([a-zA-Z]\w*)\s*=>\s*(?:(pop\(\))|(?:\((\w+)\s*,\s*([a-zA-Z]\w*)\)))(?:\s*\\\s*(\w+))?\n")
        def parse_submaquina(spec, nome, ape):

            linhas = spec.split('\n')

            # estados
            estados = re.sub(r'^[\s\t]+', r'', linhas[0]).split()

            # inicial
            inicial = re.sub(r'^[\s\t]+', r'', linhas[1])

            # estados finais
            finais = re.sub(r'^[\s\t]+', r'', linhas[2]).split()
            
            # alfabeto
            alfabeto = re.sub(r'^[\s\t]+', r'', linhas[3]).split()
            
            # Automato Transdutor
            ape.add_submaquina(nome=nome, estados=estados, estadoInicial=inicial, estadosFinais=finais, alfabeto=alfabeto)
            subm = ape[nome]

            for match_output_2 in match_transicoes.finditer(spec):
                qi, s, qj, saida = match_output_2.groups()
                subm.add_transicao(de=qi, com=s, para=qj)
                if saida is not None:
                    subm.add_saida(de=qi, com=s, saida=saida)
            for match_output_3 in match_chamadas.finditer(spec):
                qi, pop, Sj, qj, saida = match_output_3.groups()
                if pop is None:
                    subm.add_chamada_para_submaquina(de=qi, para=Sj, retorno=qj)
                    if saida is not None:
                        subm.add_saida(de=qi, com=Sj, saida=saida)
                else: # se é pop()
                    if saida is not None:
                        subm.add_saida(de=qi, com='pop', saida=saida)

        match_iter = match_automato.finditer(mo1.group(2))
        for mo in match_iter:
            nome_automato = mo.group(1)
            spec = mo.group(2)
            parse_submaquina(spec, nome_automato, ape)

        ape.set_submaquina_inicial(maquina_inicial)
        ape.gerar_alfabeto()
        return ape
