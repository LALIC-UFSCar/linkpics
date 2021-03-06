# bibliotecas do python
#from __future__ import print_function
import threading
import os
import json
import shutil
from UTIL import utils

from UTIL.crawler import Crawler
from VC.imagem import Imagem
from PLN.m_PLN import AplicadorPLN
from VC.image_process import ThreadVC
from PLN.text_process import ThreadPLN
from PLN.word_embeddings import WordEmbeding
from align_objects import AlignObjects
from align_persons import AlignPersons
import time

import shutil

class AlignTool:
    def __init__(self):
        self.w_embeddings = WordEmbeding(100)  #inicializa as word embeddings
        self.PATH_PROJETO = os.path.dirname(os.path.abspath(__file__)) + "/"
        self.crawler = Crawler()
        self.legenda = ""
        self.titulo_noticia = ""
        self.noticia = ""
        self.titulo_diretorio = ""
        self.path_imagem = ""
        self.path_legenda = ""
        self.path_noticia = ""
        self.path_titulo = ""
        self.directory = ""
        self.nome_arquivo = ""
        # self.classificador = CnnClassifier("resnet")
        self.lst_legenda = []
        self.lst_top_nomeadas_texto = []
        self.list_boundingBoxOrganizada = []
        self.lst_top_substantivos_objects = []
        self.dict_lematizado = {}
        self.noticia_sem_imagem = False
        self.total_pessoas = 0
        self.total_nomes = 0
        
        self.index_cor_bounding_box = 0
        # Red, Blue , Dark Green, Yellow, Black, Orange, Light Blue, Light Green
        self.colors_bounding_box = [(0, 0, 255),
                                    (139, 0, 0),
                                    (154, 205, 50),
                                    (0, 255, 255),
                                    (0, 0, 0),
                                    (0, 165, 255),
                                    (0, 0, 255),
                                    (255, 191, 0),
                                    (144, 238, 144)]
        
        self.colors_html = [(255, 0, 0),
                                    (0, 0, 139),
                                    (50, 205, 154),
                                    (255, 255, 0 ),
                                    (0, 0, 0),
                                    (255, 165, 0),
                                    (255, 0, 0),
                                    (0, 191, 255),
                                    (144, 238, 144)]

    def _remover_caracteres_especiais(self, titulo_noticia):
        """Remove caracteres estranhos das noticias"""
        titulo_noticia = titulo_noticia.replace('"', "")
        titulo_noticia = titulo_noticia.replace(",", "")
        titulo_noticia = titulo_noticia.replace("\n", "")
        titulo_noticia = titulo_noticia.replace("'", "")
        titulo_noticia = titulo_noticia.replace("$", "")
        return titulo_noticia

    def _limpar_arquivos(self, noticia, imagem):
        os.remove(noticia)
        #os.remove(imagem)
        # os.remove("noticia_atual/darknet_result.txt")
        # os.remove("noticia_atual/extraction_result.txt")
        #  os.remove("noticia_atual/image_result.txt")
        # os.remove("noticia_atual/image_result9000.txt")
        os.remove("noticia_atual/img_original.jpg")
        os.remove("noticia_atual/noticia.txt")
        os.remove("noticia_atual/titulo.txt")

    def _get_resources(self, url):
        encontrou_img = 0  #inicializa a variavel
        # rastreia a página
        self.nome_arquivo, self.titulo_noticia, encontrou_img = self.crawler.crawl_page(url)
        print("aq")
        if encontrou_img == 1 and os.path.exists(self.nome_arquivo):  # se achou imagem na notícia
            if self.titulo_noticia != "":  # se a noticia existe em ingles
                # le o arquivo e guarda na variavel
                self.noticia = self.crawler.file_to_variavel(self.nome_arquivo)
                # Remove caracteres estranhos das noticias
                self.titulo_noticia = self._remover_caracteres_especiais(self.titulo_noticia)

                self.titulo_diretorio = self.titulo_noticia.replace(" ", "")  #titulo do diretorio

                #grava no txt o titulo - noticias/nomenoticia/titulo.txt
                utils.escrever_arquivo(self.titulo_noticia, "noticia_atual/titulo.txt")

                #grava  a legenda da imagem--noticias/nomenoticia/caption.txt
                self.legenda = self.crawler.file_to_variavel(self.nome_arquivo + "_caption.txt")
                self.legenda = self.legenda.replace("\n", "")
                

                self.path_imagem = self.nome_arquivo + ".jpg"  # caminho da imagem original
                shutil.copy2(self.path_imagem,'static/alinhamento2.jpg')
                print("imagem copiada")
                self.path_legenda = self.nome_arquivo + "_caption.txt"  #caminho da legenda

                self.path_titulo = "noticia_atual/titulo.txt"  #caminho do título

                self.path_noticia = self.nome_arquivo  # path da noticia

                self.directory = "noticias/" + self.titulo_diretorio  #nome do diretorio que será criado

                # if os.path.exists(self.directory):  # se a noticia ainda não foi coletada
                #         shutil.rmtree(self.directory)

                if not os.path.exists(self.directory):  # se a noticia ainda não foi coletada
                    os.makedirs(self.directory)  #cria o diretorio da noticia
                    #envia a imagem original para o dir da noticia
                    os.rename(self.path_imagem, self.directory + "/img_original.jpg")
                    #envia a  noticia original para o dir da noticia
                    os.rename(self.nome_arquivo, self.directory + "/noticia.txt")
                    #envia a  legenda  para o dir da noticia
                    os.rename(self.path_legenda, self.directory + "/caption.txt")
                    #envia o titulo para o dir da noticia
                    os.rename(self.path_titulo, self.directory + "/titulo.txt")
                    # novo path da imagem original
                    self.path_imagem = self.directory + "/img_original.jpg"
                    self.path_noticia = self.directory + "/noticia.txt"  #novo path da noticia
                   

            else:  # Se a noticia não estiver em inglês
                os.remove(self.nome_arquivo + ".jpg")
                os.remove(self.nome_arquivo + "_caption.txt")
        else:
            self.noticia_sem_imagem = True



    def _set_manual_resources(self):
            self.titulo_diretorio = self.titulo_noticia.replace(" ", "")  #titulo do diretorio
            #grava no txt o titulo - noticias/nomenoticia/titulo.txt
            utils.escrever_arquivo(self.titulo_noticia, "noticia_atual/titulo.txt")
            
            shutil.copy2(self.path_imagem,'static/alinhamento2.jpg')
            print("imagem copiada")

            self.directory = "noticias/" + self.titulo_diretorio  #nome do diretorio que será criado
            utils.escrever_arquivo(self.noticia,"noticia_manual.txt")
            self.path_noticia = "noticia_manual.txt"  # path da noticia
            # if os.path.exists(self.directory):  # se a noticia ainda não foi coletada
            #             shutil.rmtree(self.directory)
            if not os.path.exists(self.directory):  # se a noticia ainda não foi coletada
                os.makedirs(self.directory)  #cria o diretorio da noticia
            shutil.copy2(self.path_imagem, self.directory + "/img_original.jpg")    
    def _process_text_image(self):
        # cria uma instancia da classe Imagem, passando o path da imagem
        print(self.directory)
        print(self.path_noticia)
        imagem = Imagem(self.path_imagem, self.directory, self.PATH_PROJETO)
        # cria uma instancia do processador de texto
        aplicador_pln = AplicadorPLN(self.PATH_PROJETO, self.noticia, self.legenda, self.titulo_noticia,
                                     self.path_noticia, self.directory, self.w_embeddings)
        
        self.lst_top_nomeadas_texto = aplicador_pln.get_list_top_entidades_nomeadas()
        
        
        print("[BEFORE]Pessoas no texto:"+str(len(self.lst_top_nomeadas_texto)))
        #####CRIA AS THREADS DE PLN E VC#####
        threads = []
        thread_pln = ThreadPLN(1, "PLN", aplicador_pln)
        thread_vc = ThreadVC(2, "VC", imagem)

        #Inicializa as threads
        thread_pln.start()
        thread_vc.start()

        threads.append(thread_pln)
        threads.append(thread_vc)
        # Espera as threads terminarem
        for t in threads:
            t.join()

        ##########################################
        # Alinhar as pessoas
        self.lst_legenda = aplicador_pln.entidades_legenda() 

        self.lst_top_nomeadas_texto = aplicador_pln.get_list_top_entidades_nomeadas()
        print("Pessoas no texto:"+str(len(self.lst_top_nomeadas_texto)))
        # print(self.lst_top_nomeadas_texto)
        self.dict_lematizado = aplicador_pln.get_dict_lematizado()
        self.list_boundingBoxOrganizada = imagem.list_boundingBoxOrganizada

        # porter_stemmer = PorterStemmer()
        # lemmatizer = WordNetLemmatizer()

        self.lst_top_substantivos_objects = aplicador_pln.lst_top_substantivos_objects
        
        # for palavra in lst_top_substantivos_objects:
        #      self.lst_top_substantivos_objects.append(lemmatizer.lemmatize(palavra))

        # print(lst_top_substantivos_objects)  
        # 
        print("--------------SUBSTANTIVOS-------------")  
        print(self.lst_top_substantivos_objects)
       
    
    

    def align_from_url(self, url, person_choose, object_choose):
        """Alinha a partir de uma url fornecida pela usuario"""
       
        try:
            self.noticia_sem_imagem = False
            self._get_resources(url)

            if self.noticia_sem_imagem is True:
                return 0
            
            print('1')
            self._process_text_image()
            print('2')

            pessoas_noticia = len(self._get_bounding_persons(self.list_boundingBoxOrganizada))
            nomes_noticia = len(self.lst_top_nomeadas_texto)

            # if pessoas_noticia == 0 or nomes_noticia == 0:
            #     return 0

            self.total_pessoas += pessoas_noticia
            self.total_nomes += nomes_noticia
            
        except Exception as e:
            print(e)

        # Alinha as pessoas
        person = AlignPersons(self.lst_legenda, self.lst_top_nomeadas_texto, self.list_boundingBoxOrganizada, self.directory + "/img_original.jpg", self.directory + "/",  self.index_cor_bounding_box, self.colors_bounding_box)
        persons_aligned = person.align(person_choose)

        if persons_aligned is None:
            persons_aligned = {}


        #O indice das cores continua de onde parou o indice realizado no alinhamento de pessoas.
        self.index_cor_bounding_box = len(persons_aligned.keys()) 

        print("INDEX -- " + str(self.index_cor_bounding_box))
        print(self.colors_bounding_box[2])
        # Alinha os objetos
        object = AlignObjects(self.lst_legenda, self.lst_top_nomeadas_texto, self.lst_top_substantivos_objects,
                              self.list_boundingBoxOrganizada, self.directory, self.dict_lematizado, self.index_cor_bounding_box, self.colors_bounding_box)
        object_aligned = object.align(object_choose)
        
        
        
        
        img_url = "static/"+self.titulo_noticia+"_"+str(person_choose)+"_"+str(object_choose)+".jpg"

        #reseta o indice
        self.index_cor_bounding_box = 0
        #Prepara o texto, legenda, titulo que serao destacados

        try:
            if persons_aligned:
                for key,value in persons_aligned.items():
                    nomes = key.split(' ')
                    # print(nomes[0])
                    # print(str(self.colors_html[self.index_cor_bounding_box]))
                    for nome in nomes:
                        self.noticia = self.noticia.replace(' '+nome,' <b style="color:rgb'+str(self.colors_html[self.index_cor_bounding_box])+'">'+nome+'</b>')
                        self.legenda = self.legenda.replace(' '+nome,' <b style="color:rgb'+str(self.colors_html[self.index_cor_bounding_box])+'">'+nome+'</b>')
                        self.titulo_noticia = self.titulo_noticia.replace(' '+nome,' <b style="color:rgb'+str(self.colors_html[self.index_cor_bounding_box])+'">'+nome+'</b>')
                    self.index_cor_bounding_box += 1    

            
            if object_aligned:
                for key,value in object_aligned.items():
                    palavra = key + " " #palavra com o espaço depois.
                    palavras= [palavra, palavra.title(), palavra.upper(), palavra.lower(),palavra+".",palavra+"?",palavra+"!",palavra+";",palavra.title()+".",palavra.title()+"?",palavra.title()+"!",palavra.title()+";",palavra.lower()+".",palavra.lower()+"?",palavra.lower()+"!",palavra.lower()+";",palavra.upper()+".",palavra.upper()+"?",palavra.upper()+"!",palavra.upper()+";"]
                    for p in palavras:
                        self.noticia = self.noticia.replace(' '+p,' <b style="color:rgb'+str(self.colors_html[self.index_cor_bounding_box])+'">'+p+'</b> ')
                        self.legenda = self.legenda.replace(' '+p,' <b style="color:rgb'+str(self.colors_html[self.index_cor_bounding_box])+'">'+p+'</b> ')
                        self.titulo_noticia = self.titulo_noticia.replace(' '+p,' <b style="color:rgb'+str(self.colors_html[self.index_cor_bounding_box])+'">'+p+'</b> ')
                    self.index_cor_bounding_box += 1

            dic_avaliação = {}
            #prepara o dicionario de avaliação
            if persons_aligned:
                for key,value in persons_aligned.items():
                    dic_avaliação[key]=''
            
            if object_aligned:
                for key,value in object_aligned.items():
                    dic_avaliação[key]=''
        except Exception as e:
            print(e)
           

        print("PROCESSO FINALIZADO")
        return persons_aligned, object_aligned, img_url, self.titulo_noticia, self.legenda, self.noticia, dic_avaliação
        
    def align_manual(self, legenda, titulo, texto, img_path, person_choose, object_choose):
        """Alinha a partir de uma url fornecida pela usuario"""
        self.titulo_noticia = titulo
        self.legenda = legenda
        self.noticia = texto
        self.path_imagem = img_path

        self._set_manual_resources()
        self._process_text_image()

        # Alinha as pessoas
        person = AlignPersons(self.lst_legenda, self.lst_top_nomeadas_texto, self.list_boundingBoxOrganizada, self.directory + "/img_original.jpg", self.directory + "/")
        persons_aligned = person.align(person_choose)

        # Alinha os objetos
        object = AlignObjects(self.lst_legenda, self.lst_top_nomeadas_texto, self.lst_top_substantivos_objects,
                              self.list_boundingBoxOrganizada)
        object_aligned = object.align(object_choose)

        
        print("PROCESSO FINALIZADO")
        
        img_url = "static/"+self.titulo_noticia+"_"+str(person_choose)+"_"+str(object_choose)+".jpg"
        return persons_aligned, object_aligned, img_url    



    def _get_bounding_persons(self, boundingBox):
        bbox_pessoas = []
        for bounding in boundingBox:
            if bounding.objeto == "person":  # Se encontrar uma pessoa
                bbox_pessoas.append(bounding)
        return bbox_pessoas


# align = AlignTool()
# align.align_from_url(
#     "http://www1.folha.uol.com.br/internacional/en/brazil/2016/05/1767623-olympic-games-will-be-a-major-success-says-rousseff.shtml",
#     2, 1)

# align = AlignTool()
# align.align_from_url(
#     "http://www1.folha.uol.com.br/internacional/en/brazil/2016/09/1809210-rousseff-asks-supreme-court-to-annul-senate-session-and-to-call-another-trial.shtml",
#     2, 1)


# align = AlignTool()
# URLS = utils.read_lines("/data/alinhador/only_people.txt")  #le o arquivo e coloca em um list de urls
# count = 0
# for url in URLS:  # varre a lista de sites
    
#         count = count + 1  # aumenta o contador de noticias
#         if count> 0:
#             print("Progresso " + str(count) + "/" + str(len(URLS))) 
#             retorno = align.align_from_url(url, 1, 1)
#             if retorno > 0:
#                 media_pessoas = align.total_pessoas / count
#                 media_nomes = align.total_nomes / count

#                 print('A media de pessoas para cada noticia eh: {}'.format(media_pessoas))
#                 print('A media de nomes para cada noticia eh: {}'.format(media_nomes))
#             else:
#                 count -= 1
#                 print('noticia zuada')        

#     #align.align_from_url(url, 1, 2)

# media_pessoas = align.total_pessoas / len(URLS)
# media_nomes = align.total_nomes / len(URLS)

# print('A media de pessoas para cada noticia eh: {}'.format(media_pessoas))
# print('A media de nomes para cada noticia eh: {}'.format(media_nomes))




# #http://www1.folha.uol.com.br/internacional/en/scienceandhealth/2016/09/1811315-new-medicine-cures-malaria-in-rodents.shtml
# #http://www1.folha.uol.com.br/internacional/en/travel/2016/02/1740667-jaguar-populations-in-the-pantanal-recovering-to-delight-of-tourists.shtml