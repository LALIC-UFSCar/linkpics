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
        self.tipo_crawler = ""

    def file_to_variavel(self, file_name):
        texto = ""
        with open(file_name, 'rt') as f:
            for line in f:
                texto = texto + line.replace('\n', '')
        return texto

    def crawl_page(self, url):
        global nome_arquivo
        nome_arquivo = 'noticia_atual/' + self.obter_nome_arquivo(url)
        path_imagem = nome_arquivo
       # path_imagem = ""
        self.coletar_img(url, path_imagem)
        titulo_noticia = ""
        if encontrou_img == 1:
            titulo_noticia = self.coletar_texto_ingles(url, nome_arquivo)
        return nome_arquivo, titulo_noticia, encontrou_img

    def obter_nome_arquivo(self, path_link):
        link_cortado = path_link.split('/')
        nome_arquivo = link_cortado[-1].split('.')
        self.tipo_crawler = link_cortado[-2]
        return nome_arquivo[0]

    def coletar_img(self, url, nome_arquivo):
        global encontrou_img
        legenda = None
        encontrou_img = 0
        page = r.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(urlopen(page).read(), "html.parser")
        if self.tipo_crawler == "news":
            dados_dentro_td = soup.findAll('figure', attrs={'class': 'media-landscape has-caption full-width lead'})
            has_caption = True
            if dados_dentro_td == []:
                has_caption = False
                dados_dentro_td = soup.findAll('figure', attrs={'class': 'media-landscape no-caption full-width lead'})

            for td in dados_dentro_td:
                imgs = td.findAll('img')
                for img in imgs:
                    url = img['src']
                    name = nome_arquivo + ".jpg"
                    urllib.request.urlretrieve(url, name)
                    break
                if has_caption is True:
                    caption = td.findAll('span', attrs={'class': 'media-caption__text'})
                    caption = caption[0].text
                    caption = caption.replace('\n','')
                    caption = caption.replace('  ','')
                    write_file(nome_arquivo + "_caption.txt", " ")
                    append_to_file(nome_arquivo + "_caption.txt", caption)
                if os.path.isfile(nome_arquivo + ".jpg"):
                        encontrou_img = 1

        if self.tipo_crawler == "story":
            dados_dentro_td = soup.findAll('div', attrs={'class': 'inline-media inline-image'})
            has_caption = True
            if dados_dentro_td == []:
                has_caption = False
                dados_dentro_td = soup.findAll('figure', attrs={'class': 'media-landscape no-caption full-width lead'})
            url = dados_dentro_td[0].contents[1].attrs['href']
            caption = dados_dentro_td[0].contents[1].attrs['title']
            name = nome_arquivo + ".jpg"
            urllib.request.urlretrieve(url, name)
            write_file(nome_arquivo + "_caption.txt", " ")
            append_to_file(nome_arquivo + "_caption.txt", caption)
            if os.path.isfile(nome_arquivo + ".jpg"):
                        encontrou_img = 1
           
            

    def coletar_texto_ingles(self, url, nome_arquivo):
        titulo_noticia = ""
        page = r.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(urlopen(page).read(), "html.parser")

        if self.tipo_crawler == "news":
            #Get TITLE
            dados_dentro_div = soup.findAll('div', attrs={'class': 'story-body'})
            link_en_ptbr = set()
            string_vazia = ''
            for div in dados_dentro_div:

                hagas1 = div.findAll('h1')
                if hagas1 !=[]:
                    for titulo in hagas1:
                        titulo_noticia = titulo.get_text()
                        break
                else:
                    hagas2 = div.findAll('h2')
                    for titulo in hagas2:
                        titulo_noticia = titulo.get_text()
                        break

            # GET TEXT
            dados_dentro_div = soup.findAll('div', attrs={'class': 'story-body__inner'})
            link_en_ptbr = set()
            string_vazia = ''
            for div in dados_dentro_div:
                paragrafos = div.findAll('p', attrs={'class': ''})
                introduction = div.findAll('p')
                # paragrafos.pop(0)
                # paragrafos.pop(0)
                # paragrafos.pop(0)
                write_file(nome_arquivo, " ")
                append_to_file(nome_arquivo, introduction[0].string)
                for p in paragrafos:
                    append_to_file(nome_arquivo, p.string)
        

        if self.tipo_crawler == "story":
              #Get TITLE
            dados_dentro_div = soup.findAll('div', attrs={'class': 'primary-header primary-header-with-context'})
            link_en_ptbr = set()
            string_vazia = ''
            for div in dados_dentro_div:

                hagas1 = div.findAll('h1')
                for titulo in hagas1:
                    titulo_noticia = titulo.get_text()
                    break

            # GET TEXT
            dados_dentro_div = soup.findAll('div', attrs={'class': 'body-content'})
            link_en_ptbr = set()
            string_vazia = ''
            for div in dados_dentro_div:
                paragrafos = div.findAll('p', attrs={'class': ''})
                # introduction = div.findAll('p')
                # paragrafos.pop(0)
                # paragrafos.pop(0)
                # paragrafos.pop(0)
                write_file(nome_arquivo, " ")
                # append_to_file(nome_arquivo, introduction[0].string)
                for p in paragrafos:
                    texto = p.text
                    init_texto= p.text[:2]
                    if init_texto != "\n\n":
                        append_to_file(nome_arquivo, texto)
            
                            
        return titulo_noticia


