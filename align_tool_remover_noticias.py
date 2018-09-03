# bibliotecas do python
#from __future__ import print_function
import threading
import os
import json
import shutil
from UTIL import utils

from UTIL.crawler_bbc import Crawler
from VC.imagem import Imagem
from PLN.m_PLN import AplicadorPLN
from VC.image_process import ThreadVC
from PLN.text_process import ThreadPLN
from PLN.word_embeddings import WordEmbeding
from align_objects import AlignObjects
from align_persons import AlignPersons


import shutil

class AlignToolObjects:
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
        self.nome_arquivo.replace('\n','')
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
                if os.path.exists(self.nome_arquivo + "_caption.txt"):
                    self.legenda = self.crawler.file_to_variavel(self.nome_arquivo + "_caption.txt")
                    self.legenda = self.legenda.replace("\n", "")
                    self.path_legenda = self.nome_arquivo + "_caption.txt"  #caminho da legenda
                else:
                    self.legenda = ""
                    self.path_legenda = ""

                self.path_imagem = self.nome_arquivo + ".jpg"  # caminho da imagem original
                shutil.copy2(self.path_imagem,'static/alinhamento2.jpg')
                print("imagem copiada")
                

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
                    if os.path.exists(self.nome_arquivo + "_caption.txt"):
                        os.rename(self.path_legenda, self.directory + "/caption.txt")
                    #envia o titulo para o dir da noticia
                    os.rename(self.path_titulo, self.directory + "/titulo.txt")
                    # novo path da imagem original
                    self.path_imagem = self.directory + "/img_original.jpg"
                    self.path_noticia = self.directory + "/noticia.txt"  #novo path da noticia
                   

            else:  # Se a noticia não estiver em inglês
                os.remove(self.nome_arquivo + ".jpg")
                if os.path.exists(self.nome_arquivo + "_caption.txt"):
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
        self.noticia_sem_imagem = False
        self._get_resources(url)

        if self.noticia_sem_imagem is True:
            return {}, {}, '', '', '', '', {}
        
        self._process_text_image()
        

        # Alinha as pessoas
        person = AlignPersons(self.lst_legenda, self.lst_top_nomeadas_texto, self.list_boundingBoxOrganizada, self.directory + "/img_original.jpg", self.directory + "/", self.index_cor_bounding_box, self.colors_bounding_box)
        persons_aligned = person.align(person_choose)

        if persons_aligned is None:
            persons_aligned = {}

        # Alinha os objetos
        object = AlignObjects(self.lst_legenda, self.lst_top_nomeadas_texto, self.lst_top_substantivos_objects,
                              self.list_boundingBoxOrganizada, self.directory, self.dict_lematizado,  self.index_cor_bounding_box, self.colors_bounding_box)
        object_aligned = object.align(object_choose)
        
        if persons_aligned != {} or object_aligned != {}:
            utils.escrever_arquivo_append(url, "noticias_filtradas/bbc news/bbc_novas_filtradas.txt")
        
        
        
       
        
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






# align = AlignTool()
# align.align_from_url(
#     "http://www1.folha.uol.com.br/internacional/en/brazil/2016/05/1767623-olympic-games-will-be-a-major-success-says-rousseff.shtml",
#     1, 1)

# align = AlignTool()
# align.align_from_url(
#     "http://www1.folha.uol.com.br/internacional/en/business/2017/09/1919476-criticized-by-environmentalist-groups-land-transactions-with-foreigners-resurface-in-brazil.shtml",
#     1, 2)


align = AlignToolObjects()
URLS = utils.read_lines("/home/erehzio/Projects/AlinhadorTextoImagem/noticias_filtradas/bbc news/bbc_filtradas.txt")  #le o arquivo e coloca em um list de urls
count = 0
for url in URLS:  # varre a lista de sites
    count = count + 1  # aumenta o contador de noticias
    if count > 0:
        print("Progresso " + str(count) + "/" + str(len(URLS))) 
        align.align_from_url(url, 2, 1)
        
    #align.align_from_url(url, 1, 2)



#http://www1.folha.uol.com.br/internacional/en/scienceandhealth/2016/09/1811315-new-medicine-cures-malaria-in-rodents.shtml
#http://www1.folha.uol.com.br/internacional/en/travel/2016/02/1740667-jaguar-populations-in-the-pantanal-recovering-to-delight-of-tourists.shtml