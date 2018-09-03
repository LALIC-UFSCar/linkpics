import re
import unicodedata


def file_to_variavel(file_name):
    texto = ""
    with open(file_name, 'rt') as f:
        for line in f:
            texto = texto + line.replace('\n', '')
    return texto


def file_to_List(file_name):
    lista = []
    with open(file_name, 'rt') as f:
        for line in f:
            lista.append(line.replace('\n', ''))
    return lista


def removerAcentosECaracteresEspeciais(palavra):
    
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)


def obter_nome_arquivo(path_link):
    link_cortado = path_link.split('/')
    nome_arquivo = link_cortado[-1].split('.')
    nome = nome_arquivo[-2]
    if len(nome) > 120:
        nome = nome[:120]
    return nome


def read_words(arquivo_txt):
    open_file = open(arquivo_txt, 'r')  #abre o arquivo
    words_list = []
    contents = open_file.readlines()  #le cada linha do arquivo
    for line in contents:
        words_list.extend(line.split())
    open_file.close()
    return words_list


def read_lines(arquivo_txt):
    open_file = open(arquivo_txt, 'r')  #abre o arquivo
    line_list = []
    contents = open_file.readlines()  #le cada linha do arquivo
    for line in contents:
        line_list.append(line)
    open_file.close()
    return line_list


def escrever_arquivo(texto, nome_arquivo):
    f = open(nome_arquivo, 'w')
    f.write(texto)
    f.close()


def escrever_arquivo_append(texto, nome_arquivo):
    f = open(nome_arquivo, 'a')
    f.write(texto)
    f.close()


def escrever_arquivo_from_list(list, nome_arquivo):
    f = open(nome_arquivo, 'w')
    for l in list:
        f.write(l + "\n")
    f.close()


