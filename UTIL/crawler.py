from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import socket
from .general import *
from .domain import *
import urllib.request as r


class Crawler(object):

    encontrou_img = 0  #inicia zerada
    socket.setdefaulttimeout(70)  # para evitar time out na página rastreada
    nome_arquivo = ""

    def __init__(self):
        self.noticia = ""

    def file_to_variavel(self, file_name):
        texto = ""
        with open(file_name, 'rt') as f:
            for line in f:
                texto = texto + line.replace('\n', '')
        return texto

    def crawl_page(self, url):
        global nome_arquivo
        nome_arquivo = 'noticia_atual/' + self.obter_nome_arquivo(url)
        path_imagem = 'noticia_atual/' + self.obter_nome_arquivo(url)
        self.coletar_img(url, path_imagem)
        titulo_noticia = ""
        if encontrou_img == 1:
            titulo_noticia = self.coletar_texto_ingles(url, nome_arquivo)
        return nome_arquivo, titulo_noticia, encontrou_img

    def obter_nome_arquivo(self, path_link):
        link_cortado = path_link.split('/')
        nome_arquivo = link_cortado[-1].split('.')
        nome = nome_arquivo[-2]
        if len(nome) > 120:
            nome = nome[:120]
        return nome

    def coletar_img(self, url, nome_arquivo):
        global encontrou_img
        legenda = None
        encontrou_img = 0
        page = r.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(urlopen(page).read(), "html.parser")
        dados_dentro_td = soup.findAll('td', attrs={'class': 'articleGraphicImage'})
        dados_td_caption = soup.findAll('td', attrs={'class': 'articleGraphicCaption'})
        if len(dados_td_caption) > 0:
            legenda = dados_td_caption[0].text
        for td in dados_dentro_td:
            imgs = td.findAll('img')
            for img in imgs:
                url = img['src']
                name = nome_arquivo + ".jpg"
                urllib.request.urlretrieve(url, name)

                caption = legenda
                write_file(nome_arquivo + "_caption.txt", " ")
                append_to_file(nome_arquivo + "_caption.txt", caption)
                if os.path.isfile(nome_arquivo + ".jpg"):
                    encontrou_img = 1

        dados_dentro_paragrafo = soup.findAll('p', attrs={'class': 'gallery'})
        for p in dados_dentro_paragrafo:
            imgs = p.findAll('img')
            for img in imgs:
                url = img['src']
                name = nome_arquivo + ".jpg"
                urllib.request.urlretrieve(url, name)

    def coletar_texto_ingles(self, url, nome_arquivo):
        titulo_noticia = ""
        page = r.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(urlopen(page).read(), "html.parser")

        dados_dentro_div = soup.findAll('div', attrs={'class': 'double_column'})
        link_en_ptbr = set()
        string_vazia = ''
        for div in dados_dentro_div:

            hagas1 = div.findAll('h1')
            for titulo in hagas1:
                titulo_noticia = titulo.get_text()

            paragrafos = div.findAll('p')
            paragrafos.pop(0)
            paragrafos.pop(0)
            paragrafos.pop(0)

            for p in paragrafos:
                tags = p.findAll('a')
                for a in tags:
                    if get_domain_name(a['href']) == "www1.folha.uol":
                        link_en_ptbr.add(a['href'])

            if len(link_en_ptbr) > 0:
                valor_link = link_en_ptbr.pop()
                if valor_link is not string_vazia:
                    # cria o arquivo de texto
                    print('criando')
                    write_file(nome_arquivo, " ")
                    for p in paragrafos:
                        append_to_file(nome_arquivo, p.string)
                        # cria o arquivo de texto em portugues
                        # coletar_texto_portugues(valor_link, nome_arquivo)
        return titulo_noticia
