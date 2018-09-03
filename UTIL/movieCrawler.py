# bibliotecas do python
from __future__ import print_function

# from __builtin__ import list
from math import sqrt
from palavra import Palavra
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import socket
from general import *
from domain import *
import urllib.request as r
from Imagem import Imagem
import subprocess
import threading
import time
from nltk.corpus import wordnet as wn
from WordNetClasses import *
from WordEmbeddings import WordEmbeding
import utils
import operator
import trocarnomes
import requests
exitFlag = 0


socket.setdefaulttimeout(70)  # para evitar time out na página rastreada

nome_arquivo = ""  # armazena o nome do arquivo
titulo_noticia = ""  # para armazenar o título da notícia
encontrou_img= 0 #inicia zerada

def file_to_variavel(file_name):
    texto = ""
    with open(file_name, 'rt') as f:
        for line in f:
            texto = texto + line.replace('\n', '')
    return texto


def crawl_page(url):
    
    nome_arquivo = "oi"

    #coletar_img(url, path_imagem)
    #if encontrou_img == 1:
    #url= 'http://www1.folha.uol.com.br/internacional/en/
    coletar_LinksImagens(url, nome_arquivo)
   


def obter_nome_arquivo(path_link):
    link_cortado = path_link.split('/')
    nome_arquivo = link_cortado[-1].split('.')
    nome = nome_arquivo[-2]
    if len(nome) > 120:
        nome = nome[:120]
    return nome


def coletar_img(url):
    # Para cada link, obter a lista dos links de cada imagem.
    #url= 'https://film-grab.com/'
    global img_id
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c,"lxml")
#    page = r.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    #soup = BeautifulSoup(urlopen(page).read(), "html.parser")
    lst_imagens=[]
    print(url)
    dados_dentro_div = soup.findAll('div')
    x = 0
    for div in dados_dentro_div:
       imgs = div.findAll('img')
      
       for img in imgs:
         if x==0:
           url = img['src']
           print(str(img_id))
           name = "movie/"+str(img_id)+".jpg"
           urllib.request.urlretrieve(url, name)
           x = x + 1
  
  
def coletar_LinksImagens(url, nome_arquivo):
    global titulo_noticia
    global img_id
    #url= 'https://film-grab.com/2017/03/31/tale-of-tales/'
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c,"lxml")
#    page = r.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    #soup = BeautifulSoup(urlopen(page).read(), "html.parser")
    lst_imagens=[]
    print(url)
    dados_dentro_div = soup.findAll('dl')
    for div in dados_dentro_div:

        dt_list = div.findAll('dt')
        for dt in dt_list:
            a_list = dt.findAll('a')
            for a in a_list:
                lst_imagens.append(a['href'])                
    #pega a lista de links e coleta a imagem dentro dela
    
    for link in lst_imagens:
            coletar_img(link)
            img_id = img_id + 1
            



# ------------------------------------------- I N I C I O --D O ---P R O G R A M A------------------------------------------
def _LimparArquivos(noticia,imagem):
    os.remove(noticia)
    #os.remove(imagem)
   # os.remove("noticia_atual/darknet_result.txt")
   # os.remove("noticia_atual/extraction_result.txt")
  #  os.remove("noticia_atual/image_result.txt")
   # os.remove("noticia_atual/image_result9000.txt")
    os.remove("noticia_atual/img_original.jpg")
    os.remove("noticia_atual/noticia.txt")
    os.remove("noticia_atual/titulo.txt")




texto = ""
img_id = 0

# print(wn.synsets(list_palavras_wordnet[i], pos=wn.NOUN))

list_urls= utils.read_lines("crawled_movies.txt")  #le o arquivo e coloca em um list de urls
count=0
for url in list_urls: # varre a lista de sites
  count = count + 1 # aumenta o contador de noticias
  if count>0: # se count for maior que X faça
   print("Progresso "+str(count)+"/"+str(len(list_urls)))  #mostra o progresso total de noticias
   url= url.replace('\n','')
   crawl_page(url)  # rastreia a página
   