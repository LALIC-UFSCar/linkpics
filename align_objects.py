import cv2
import os
import operator
from PLN.trocar_nomes import *
from nltk.corpus import wordnet as wn
from PLN.WordNetClasses import *
from math import sqrt
from PLN.word_embeddings import WordEmbeding
from UTIL import utils
from collections import deque


class AlignObjects:
    def __init__(self, lst_legenda, lst_top_nomeadas_texto, lst_substantivos,
                 list_boundingBoxOrganizada, path_folder, dict_lematizado, index_cor_bounding_box, colors_bounding_box):
        self.lst_legenda = lst_legenda
        self.lst_top_nomeadas_texto = lst_top_nomeadas_texto
        self.lst_substantivos = lst_substantivos
        self.list_boundingBoxOrganizada = list_boundingBoxOrganizada
        self.path_folder = path_folder
        self.dict_lematizado = dict_lematizado
        self.index_cor_bounding_box = index_cor_bounding_box
        self.colors_bounding_box = colors_bounding_box

    def align(self, object_choosed):

        if object_choosed == 1:
            return self._experiment_1()

        elif object_choosed == 2:
            return self._experiment_2()

        elif object_choosed == 3:
            return self._experiment_3()

        if object_choosed == 4:
            return self._experiment_4()

        elif object_choosed == 5:
            return self._experiment_5()

        elif object_choosed == 6:
            return self._experiment_6()

        else:
            return None


    def read_words_visual(self, arquivo_txt):
        open_file = open(arquivo_txt, 'r')
        words_list = []
        contents = open_file.readlines()
        for content in contents:
            content = content.replace('\n','')
            if content not in words_list:
                words_list.append(content)
        open_file.close()
        return words_list

    def _get_bounding_objects(self):
        bbox_objects = []
        for bounding in self.list_boundingBoxOrganizada:
            if bounding.objeto != "person":  # Se encontrar uma pessoa
                bbox_objects.append(bounding)
        return bbox_objects

    def _ordenar_bbox_tamanho(self, bbox_objects):

        ordered_bbox = []
        numero_repeticoes = len(bbox_objects)  # pega o total de bounding box
        count = 0
        while count < numero_repeticoes:
            maior_area = 0
            indice_maior_area = -1
            total_bounding = len(bbox_objects)  # total de bounding box restantes

            for i in range(0, total_bounding):
                area = bbox_objects[i].width * bbox_objects[i].height
                if area > maior_area:
                    maior_area = area  #guarda a menor distancia
                    indice_maior_area = i  #guarda o indice da menor distancia

            ordered_bbox.append(bbox_objects[
                indice_maior_area])  # coloca na lista o Bounding box de menor distancia
            ordered_bbox[count].area = maior_area
            ordered_bbox[count].imagem = count
            bbox_objects.remove(bbox_objects[indice_maior_area])
            count = count + 1
        return ordered_bbox

    def _experiment_5(self):
        """ Tamanho do objeto com a palavra melhor classificada """
        print('experimento 5')
        bbox_objects = self._get_bounding_objects()
        bbox_objects = self._ordenar_bbox_tamanho(bbox_objects)

        img_original = cv2.imread("static/alinhamento2.jpg")
        texto = ""
        dic_json = {}
        num_objeto = 0
        
        #return dic_json
        while len(bbox_objects) > 0 and len(self.lst_substantivos) > 0:
            try:
                palavra = self.lst_substantivos[0]
                #texto += entidade.palavra + "= " + str(bbox_pessoas[0].imagem) + "\n"
            # num_objeto += 1
                palavra_radio_button = palavra.replace(" ","_")
                dic_json[palavra] = '<label><input type="radio" value="sim" name="radio_'+palavra_radio_button+'">Sim</label><span style="margin: 0 10px 0 10px;"></span>  <label><input type="radio"  value="nao" name="radio_'+palavra_radio_button+'">Não</label>'

                # dic_json[palavra] = "Objeto " + str(num_objeto)
                x, y, w, h = bbox_objects[0].Rect()

                #draw bounding box in img_original
                cv2.rectangle(img_original, (x, y), (x + w, y + h), self.colors_bounding_box[self.index_cor_bounding_box], 2)
                self.index_cor_bounding_box += 1
                #remove a pessoa e a bounding box
                self.lst_substantivos.pop(0)
                bbox_objects.pop(0)
            except Exception as e:
                print(e)

     
       
        cv2.imwrite("static/" + "alinhamento2.jpg", img_original)
        return dic_json

    def _experiment_6(self):
        """ WUP com cada objeto detectado """
        img_original = cv2.imread("static/alinhamento2.jpg")
        bbox_objects = self._get_bounding_objects()
        dic_alinhamento = {}

        for bbox in bbox_objects:
            index_maior_palavra = 0
            palavra_bbox = bbox.objeto  # obtém a palavra que está na Bbox
            palavra_bbox = TrocarNomes(palavra_bbox)
            dicionario_distancias_wup = {
            }  # dicionario para calcular as distancias da palavra da Bbox para todos substantivos

            for i in range(0, len(self.lst_substantivos)):
                substantivo = self.lst_substantivos[i]
                lst_synsets = wn.synsets(substantivo, pos=wn.NOUN)

                maior_distancia = 0
                for j in range(0, len(lst_synsets)):
                    synset = str(lst_synsets[j])  #pega um dos synsets referentes ao substantivo
                    synset = synset.replace("Synset('", "")
                    synset = synset.replace("')", "")
                    word = wn.synset(synset)

                    word_bounding = TrazerSynsetBoundingBox(palavra_bbox)  #synset da bbox
                    try:
                        distancia_wup = word.wup_similarity(word_bounding)
                    except:
                        distancia_wup = 0
                    if distancia_wup > maior_distancia:
                        maior_distancia = distancia_wup
                        index_maior_palavra = i

                dicionario_distancias_wup[substantivo] = maior_distancia

            sorted_wup = sorted(
                dicionario_distancias_wup.items(), key=operator.itemgetter(1), reverse=True)
            # ordena o dicionario de acordo com maior distancia
            texto = ""
            for z in range(0, 5):
                try:
                    # print(sorted_wup[z][0] + "\n")
                    texto += sorted_wup[z][0] + "\n"
                except:
                    print("erro")
            # utils.escrever_arquivo(texto, dir_objeto + arquivo_wup)
            texto = ""
            for z in range(0, 5):
                try:
                    texto += sorted_wup[z][0] + ";" + str(sorted_wup[z][1]) + "\n"
                except:
                    print("erro")
            print(texto)
            # utils.escrever_arquivo(texto, dir_objeto + arquivo_wup_medidas)
            dic_alinhamento[sorted_wup[0][0]] = palavra_bbox

        dic_json = {}
        num_objeto = 0
        for palavra, value in dic_alinhamento.items():
            num_objeto += 1
            dic_json[palavra] = "Objeto " + str(num_objeto)
            x, y, w, h = bbox_objects[0].Rect()

            #draw bounding box in img_original
            cv2.rectangle(img_original, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img_original, "Objeto" + str(num_objeto), (x + 15, y + 30),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.9, (0, 255, 0), 1)

            #remove a bounding box
            bbox_objects.pop(0)

        cv2.imwrite("static/" + "alinhamento2.jpg", img_original)
        return dic_json

    def _experiment_3(self):
        """WE com cada objeto detectado """

        img_original = cv2.imread("static/alinhamento2.jpg")
        bbox_objects = self._get_bounding_objects()
        dic_alinhamento = {}

        w_embeddings = WordEmbeding(100)  #inicializa as word embeddings
        w_embeddings.CarregarWordEmbeddings()

        for bbox in bbox_objects:

            index_maior_palavra = 0
            palavra_bbox = bbox.objeto  # obtém a palavra que está na Bbox
            print(palavra_bbox)
            palavra_bbox = TrocarNomes(palavra_bbox)

            w = WordEmbeding(100)  # instancia a classe wordEmbedding
            maior_distancia = 0
            index_maior_palavra = 0

            for i in range(0, len(self.lst_substantivos)):  #coloca todos substantivos em Lower Case
                self.lst_substantivos[i] = self.lst_substantivos[i].lower()
            self.lst_substantivos.sort()  # Organiza os substantivos por ordem alfabética

            palavra_vec_yolo = w.RetornarVetor(
                palavra_bbox)  #retorna a WOrd Embedding da palavra da Bbox
            dicionario_embeddings = w.RetornarDicionario(
                self.lst_substantivos)  #gera e obtém todas W Embeddings dos substantivos
            dicionario_distancias = {
            }  #dicionario para calcular as distancias da palavra da Bbox para todos substantivos

            for subst in self.lst_substantivos:  # para cada substantivo
                distancia_yolo = 0
                for x in range(0,
                               100):  # Calcula a distância entre a Wvec_palavra e substantivo_vec
                    try:
                        distancia_yolo = distancia_yolo + (
                            dicionario_embeddings[subst][x] - palavra_vec_yolo[x])**2
                    except:
                        continue
                distancia_yolo = sqrt(distancia_yolo)
                dicionario_distancias[subst] = distancia_yolo  #armazena no dicionario a distância
            sorted_we = sorted(
                dicionario_distancias.items(),
                key=operator.itemgetter(1))  # ordena o dicionario de acordo com menor distancia
            texto = ""
            for z in range(0, 5):  #prepara o texto do arquivo
                try:
                    texto += sorted_we[z][0] + "\n"
                except:
                    print("erro")
            # utils.escrever_arquivo(texto, dir_objeto + arquivo_embedding)
            texto = ""
            for z in range(0, 5):  #prepara o texto do arquivo
                try:
                    texto += sorted_we[z][0] + ";" + str(sorted_we[z][1]) + "\n"

                except:
                    print("erro")
            print(texto)
            # utils.escrever_arquivo(texto, dir_objeto + arquivo_wup_medidas)
            dic_alinhamento[sorted_we[0][0]] = palavra_bbox

        dic_json = {}
        num_objeto = 0
        for palavra, value in dic_alinhamento.items():
            num_objeto += 1
            dic_json[palavra] = "Objeto " + str(num_objeto)
            x, y, w, h = bbox_objects[0].Rect()

            #draw bounding box in img_original
            cv2.rectangle(img_original, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img_original, "Objeto" + str(num_objeto), (x + 15, y + 30),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.9, (0, 255, 0), 1)

            #remove a bounding box
            bbox_objects.pop(0)

        cv2.imwrite("static/" + "alinhamento2.jpg", img_original)
        return dic_json

    def _experiment_4(self):
        """ (3 CNN + classe YOLO) -> Se alguma palavra do texto letamizada ou não aparecere entre as 16 sugeridas pelas CNNS -> Alinha """
        img_original = cv2.imread("static/alinhamento2.jpg")
        bbox_objects = self._get_bounding_objects()
        dic_alinhamento = {}

        for bbox in bbox_objects:
            bbox.lst_cnn.append(bbox.objeto)
            for palavra in self.lst_substantivos:
                if palavra in bbox.lst_cnn:
                    dic_alinhamento[palavra] = palavra
                    break

        num_objeto = 0
        dic_json = {}

        for palavra, value in dic_alinhamento.items():
            num_objeto += 1
            dic_json[palavra] = "Objeto " + str(num_objeto)
            x, y, w, h = bbox_objects[0].Rect()

            #draw bounding box in img_original
            cv2.rectangle(img_original, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img_original, "Objeto" + str(num_objeto), (x + 15, y + 30),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.9, (0, 255, 0), 1)

            #remove a bounding box
            bbox_objects.pop(0)

        cv2.imwrite("static/" + "alinhamento2.jpg", img_original)
        return dic_json

    def _experiment_1(self):
        """Experimento 4 + Experimento 2"""
        arquivo_wup = "/wup_top5.txt"
        img_original = cv2.imread("static/alinhamento2.jpg")
        bbox_objects = self._get_bounding_objects()
        dic_alinhamento = {}
        num_objeto = 0
        lst_palavras_visuais = self.read_words_visual("visual_words.txt")

        for bbox in bbox_objects:
            bbox.lst_cnn.append(bbox.objeto)

        #     for palavra in self.lst_substantivos:
        #         if palavra in bbox.lst_cnn:
        #             dic_alinhamento[palavra] = num_objeto
        #             num_objeto += 1
        #             break

        dic_json = {}

        # for palavra, value in dic_alinhamento.items():

        #     dic_json[palavra] = "Objeto " + str(dic_alinhamento[palavra])
        #     x, y, w, h = bbox_objects[0].Rect()

        #     #draw bounding box in img_original
        #     cv2.rectangle(img_original, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #     cv2.putText(img_original, "Objeto" + str(dic_alinhamento[palavra]), (x + 15, y + 30),
        #                 cv2.FONT_HERSHEY_TRIPLEX, 0.9, (0, 255, 0), 1)

        #     #remove a bounding box
        #     print("REMOVIDA:" + palavra)
        #     bbox_objects.pop(0)

        # cv2.imwrite("static/" + "alinhamento2.jpg", img_original)
        # img_original = cv2.imread("static/alinhamento2.jpg")
        #bbox_objects = self._get_bounding_objects()

        #               S I M I L A R I D A D E       W U P
        dic_alinhamento = {}

        if not bbox_objects:
             return dic_json

        for bbox in bbox_objects:
            #cria uma pasta com nome {num_foto-nome_objeto}
            object_name = str(bbox.imagem) + "-" + bbox.objeto  
            if not os.path.exists(self.path_folder + "/" + object_name):
                os.mkdir(self.path_folder + "/" + object_name)  
            dir_objeto = self.path_folder + "/" + object_name

            # dicionario para calcular as distancias da palavra da Bbox para todos substantivos
            dicionario_distancias_wup = {}
            index_maior_palavra = 0
            palavra_ranqueada = ""
            distancia_ranqueada = 0

            for substantivo in self.lst_substantivos:
                maior_distancia = 0
                lst_synsets = wn.synsets(substantivo, pos=wn.NOUN)
                for j in range(0, len(lst_synsets)):
                    #pega um dos synsets referentes ao substantivo
                    synset = str(lst_synsets[j])
                    synset = synset.replace("Synset('", "")
                    synset = synset.replace("')", "")
                    word_substantivo = wn.synset(synset)
                    for palavra in bbox.lst_cnn:
                        palavra_bbox = palavra  # obtém a palavra que está na Bbox
                        palavra_bbox = TrocarNomes(palavra_bbox)
                        word_bounding = TrazerSynsetBoundingBox(palavra_bbox)  #synset da bbox

                        if word_bounding is None:
                            lst_synsets_cnn = wn.synsets(palavra_bbox, pos=wn.NOUN)
                            for k in range(0, len(lst_synsets_cnn)):
                                synset = str(lst_synsets_cnn[
                                    k])  #pega um dos synsets referentes ao substantivo
                                synset = synset.replace("Synset('", "")
                                synset = synset.replace("')", "")
                                word_bounding = wn.synset(synset)

                                try:
                                    distancia_wup = word_substantivo.wup_similarity(word_bounding)

                                except:
                                    distancia_wup = 0
                                if distancia_wup > maior_distancia:
                                    maior_distancia = distancia_wup
                                    # index_maior_palavra = i
                                    #palavra_ranqueada = substantivo
                        else:
                            try:
                                    distancia_wup = word_substantivo.wup_similarity(word_bounding)

                            except:
                                distancia_wup = 0
                                if distancia_wup > maior_distancia:
                                    maior_distancia = distancia_wup
                dicionario_distancias_wup[substantivo] = maior_distancia

            sorted_wup = sorted(
                dicionario_distancias_wup.items(), key=operator.itemgetter(1), reverse=True)
            
            wup_deque = deque()
      
            
            palavra_ranqueada = sorted_wup[0][0]
            
            #para cada palavra da sorted wup (0 a 4)
            if sorted_wup[0][0] not in lst_palavras_visuais:
                for z in range(0, 5):
                    try:
                        #verifica se esta na lista das palavras visuais
                        if sorted_wup[z][0].lower() in lst_palavras_visuais:
                            wup_deque.appendleft(sorted_wup[z][0])
                        else:
                            wup_deque.append(sorted_wup[z][0])
                    except:
                        pass
                    
                    # se estiver sobe uma posicao na lista
                palavra_ranqueada = wup_deque[0]    


            dic_alinhamento[palavra_ranqueada] = num_objeto
            num_objeto += 1
            print(maior_distancia)
            print(palavra_ranqueada)
            # ESCREVE NO DIRETORIO O TOP-5
            top5 = ""
            for z in range(0, 5):
                try:
                    top5 += self.dict_lematizado[sorted_wup[z][0].lower()] + "-------"+str(sorted_wup[z][1])+"\n"
                except:
                    pass
            utils.escrever_arquivo(top5, dir_objeto + arquivo_wup)
           

        # _________________ALINHAMENTO________________
        for palavra, value in dic_alinhamento.items():
            # dic_json[palavra] = "Objeto " + str(dic_alinhamento[palavra])
            palavra_radio_button = palavra.replace(" ","_")
            dic_json[palavra] = '<label><input type="radio" value="sim" name="radio_'+palavra_radio_button+'">Sim</label><span style="margin: 0 10px 0 10px;"></span>  <label><input type="radio"  value="nao" name="radio_'+palavra_radio_button+'">Não</label>'
            x, y, w, h = bbox_objects[0].Rect()
            size_caracters = len(palavra) * 15
            
            #draw bounding box in img_original


            cv2.rectangle(img_original, (x, y), (x + w, y + h), self.colors_bounding_box[self.index_cor_bounding_box], 2)
            # cv2.rectangle(img_original,(x,y),(x + size_caracters, y + 30),(0,0,0),thickness=-1)
            # cv2.putText(img_original, palavra, (x + 3, y + 20),
            #             cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
            self.index_cor_bounding_box += 1

            #remove a bounding box
            bbox_objects.pop(0)

        cv2.imwrite("static/" + "alinhamento2.jpg", img_original)
        return dic_json

    def _experiment_2(self):
        """Experimento 4 + Experimento  3 """
        arquivo_embedding = "/embedding_top5.txt"
        img_original = cv2.imread("static/alinhamento2.jpg")
        bbox_objects = self._get_bounding_objects()
        dic_alinhamento = {}
        lst_palavras_visuais = self.read_words_visual("visual_words.txt")
        num_objeto = 0

        # for bbox in bbox_objects:
        #     bbox.lst_cnn.remove('torch')
        #     bbox.lst_cnn.append(bbox.objeto)

        #     for palavra in self.lst_substantivos:
        #         if palavra in bbox.lst_cnn:

        #             dic_alinhamento[palavra] = num_objeto
        #             num_objeto += 1
        #             break

        dic_json = {}

        # for palavra, value in dic_alinhamento.items():

        #     dic_json[palavra] = "Objeto " + str(dic_alinhamento[palavra])
        #     x, y, w, h = bbox_objects[0].Rect()

        #     #draw bounding box in img_original
        #     cv2.rectangle(img_original, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #     cv2.putText(img_original, "Objeto" + str(dic_alinhamento[palavra]), (x + 15, y + 30),
        #                 cv2.FONT_HERSHEY_TRIPLEX, 0.9, (0, 255, 0), 1)

        #     #remove a bounding box
        #     print("REMOVIDA:" + palavra)
        #     bbox_objects.pop(0)

        # cv2.imwrite("static/" + "alinhamento2.jpg", img_original)
        # img_original = cv2.imread("static/alinhamento2.jpg")
        #bbox_objects = self._get_bounding_objects()
        dic_alinhamento = {}

        #  A P L I C A Ç Ã O  - W O R D   E M B E D D I N G S
        # w_embeddings = WordEmbeding(100)  #inicializa as word embeddings
        # w_embeddings.CarregarWordEmbeddings()
        dic_top_5 = {}
        # coloca todos substantivos em Lower Case e
        # Organiza os substantivos por ordem alfabética
        for i in range(0, len(self.lst_substantivos)):
            self.lst_substantivos[i] = self.lst_substantivos[i].lower()
        self.lst_substantivos.sort()

        #gera e obtém todas W Embeddings dos substantivos
        w = WordEmbeding(100)  # instancia a classe wordEmbedding
        w.CarregarWordEmbeddings()
        dicionario_embeddings = w.RetornarDicionario(self.lst_substantivos)
        palavra_ranqueada = ""
        
        if not bbox_objects:
            return dic_json

        for bbox in bbox_objects:
            #cria uma pasta com nome {num_foto-nome_objeto}
            object_name = str(bbox.imagem) + "-" + bbox.objeto  
            if not os.path.exists(self.path_folder + "/" + object_name):
                os.mkdir(self.path_folder + "/" + object_name)  
            dir_objeto = self.path_folder + "/" + object_name
            index_maior_palavra = 0
            palavra_ranqueada = ""
            distancia_ranqueada = 100
            #dicionario para calcular as distancias da palavra da Bbox para todos substantivos
            dicionario_distancias = {}

            for substantivo in self.lst_substantivos:  # para cada substantivo
                for palavra in bbox.lst_cnn:
                    palavra_bbox = palavra  # obtém a palavra que está na Bbox
                    palavra_bbox = TrocarNomes(palavra_bbox)

                    maior_distancia = 0
                    index_maior_palavra = 0

                    #retorna a WOrd Embedding da palavra da Bbox
                    embedding_cnn = w.RetornarVetor(palavra_bbox)
                    if embedding_cnn is None:
                        continue

                    if substantivo not in dicionario_embeddings:
                        continue

                    if dicionario_embeddings[substantivo] is None:
                        continue

                    distancia_we = 0
                    # Calcula a distância entre a Wvec_palavra e substantivo_vec
                    for x in range(0, 100):
                        try:
                            distancia_we = distancia_we + (
                                dicionario_embeddings[substantivo][x] - embedding_cnn[x])**2
                        except:
                            continue
                    distancia_we = sqrt(distancia_we)
                    # armazena no dicionario a distância
                    dicionario_distancias[palavra_bbox] = distancia_we

                # ordena o dicionario de acordo com menor distancia
                sorted_we = sorted(dicionario_distancias.items(), key=operator.itemgetter(1))
                # texto = ""
                # for z in range(0, 5):  #prepara o texto do arquivo
                #     try:
                #         texto += sorted_we[z][0] + "\n"
                #     except:
                #         pass
                # utils.escrever_arquivo(texto, dir_objeto + arquivo_embedding)
        
                if sorted_we:
                    if sorted_we[0][1] < distancia_ranqueada:
                        distancia_ranqueada = sorted_we[0][1]
                        palavra_ranqueada = substantivo
                    dic_top_5[substantivo] = sorted_we[0][1]
               

                # ordena o dicionario de acordo com menor distancia
            sorted_we = sorted(dic_top_5.items(), key=operator.itemgetter(1))
            if sorted_we[0][0] not in lst_palavras_visuais:
                we_deque = deque()
                for z in range(0, 5):
                    try:
                        #verifica se esta na lista das palavras visuais
                        if sorted_we[z][0].lower() in lst_palavras_visuais:
                            we_deque.appendleft(sorted_we[z][0])
                        else:
                            we_deque.append(sorted_we[z][0])
                    except:
                        pass
                    
                    # se estiver sobe uma posicao na lista
                palavra_ranqueada = we_deque[0]   




            if palavra_ranqueada != '':
                dic_alinhamento[palavra_ranqueada] = num_objeto
                num_objeto += 1
                print(palavra_ranqueada)
            # ESCREVE NO DIRETORIO O TOP-5
            top5 = ""
            for z in range(0, 5):
                try:
                    top5 += self.dict_lematizado[sorted_we[z][0]] +"-------"+str(sorted_we[z][1])+"\n"
                except:
                    pass
            utils.escrever_arquivo(top5, dir_objeto + arquivo_embedding)

        for palavra, value in dic_alinhamento.items():

            # dic_json[palavra] = "Objeto " + str(dic_alinhamento[palavra])
            palavra_radio_button = palavra.replace(" ","_")
            dic_json[palavra] = '<label><input type="radio" value="sim" name="radio_'+palavra_radio_button+'">Sim</label><span style="margin: 0 10px 0 10px;"></span>  <label><input type="radio"  value="nao" name="radio_'+palavra_radio_button+'">Não</label>'
            x, y, w, h = bbox_objects[0].Rect()

            # size_caracters = len(palavra) * 15
            #draw bounding box in img_original
            cv2.rectangle(img_original, (x, y), (x + w, y + h), self.colors_bounding_box[self.index_cor_bounding_box], 2)
            # cv2.rectangle(img_original,(x,y),(x + size_caracters, y + 30),(0,0,0),thickness=-1)
            # cv2.putText(img_original, palavra, (x + 3, y + 20),
            #             cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
            self.index_cor_bounding_box += 1

            #remove a bounding box
            bbox_objects.pop(0)

        cv2.imwrite("static/" + "alinhamento2.jpg", img_original)
        return dic_json

    def _experiment_7(self):
        """Experimento 4 + Experimento 3 + Experimento 1"""
        img_original = cv2.imread("static/alinhamento2.jpg")
        bbox_objects = self._get_bounding_objects()
        dic_alinhamento = {}

        for bbox in bbox_objects:
            bbox.lst_cnn.append(bbox.objeto)
            for palavra in self.lst_substantivos:
                if palavra in bbox.lst_cnn:
                    dic_alinhamento[palavra] = palavra
                    break

        num_objeto = 0
        dic_json = {}

        for palavra, value in dic_alinhamento.items():
            num_objeto += 1
            dic_json[palavra] = "Objeto " + str(num_objeto)
            x, y, w, h = bbox_objects[0].Rect()

            #draw bounding box in img_original
            cv2.rectangle(img_original, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img_original, "Objeto" + str(num_objeto), (x + 15, y + 30),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.9, (0, 255, 0), 1)

            #remove a bounding box
            bbox_objects.pop(0)
            self.lst_substantivos.remove(palavra)

        cv2.imwrite("static/" + "alinhamento2.jpg", img_original)
        img_original = cv2.imread("static/alinhamento2.jpg")
        bbox_objects = self._get_bounding_objects()
        dic_alinhamento = {}

        w_embeddings = WordEmbeding(100)  #inicializa as word embeddings
        w_embeddings.CarregarWordEmbeddings()

        for bbox in bbox_objects:

            index_maior_palavra = 0
            palavra_bbox = bbox.objeto  # obtém a palavra que está na Bbox
            print(palavra_bbox)
            palavra_bbox = TrocarNomes(palavra_bbox)

            w = WordEmbeding(100)  # instancia a classe wordEmbedding
            maior_distancia = 0
            index_maior_palavra = 0

            for i in range(0, len(self.lst_substantivos)):  #coloca todos substantivos em Lower Case
                self.lst_substantivos[i] = self.lst_substantivos[i].lower()
            self.lst_substantivos.sort()  # Organiza os substantivos por ordem alfabética

            palavra_vec_yolo = w.RetornarVetor(
                palavra_bbox)  #retorna a WOrd Embedding da palavra da Bbox
            dicionario_embeddings = w.RetornarDicionario(
                self.lst_substantivos)  #gera e obtém todas W Embeddings dos substantivos
            dicionario_distancias = {
            }  #dicionario para calcular as distancias da palavra da Bbox para todos substantivos

            for subst in self.lst_substantivos:  # para cada substantivo
                distancia_yolo = 0
                for x in range(0,
                               100):  # Calcula a distância entre a Wvec_palavra e substantivo_vec
                    try:
                        distancia_yolo = distancia_yolo + (
                            dicionario_embeddings[subst][x] - palavra_vec_yolo[x])**2
                    except:
                        continue
                distancia_yolo = sqrt(distancia_yolo)
                dicionario_distancias[subst] = distancia_yolo  #armazena no dicionario a distância
            sorted_we = sorted(
                dicionario_distancias.items(),
                key=operator.itemgetter(1))  # ordena o dicionario de acordo com menor distancia
            texto = ""
            for z in range(0, 5):  #prepara o texto do arquivo
                try:
                    texto += sorted_we[z][0] + "\n"
                except:
                    print("erro")
            # utils.escrever_arquivo(texto, dir_objeto + arquivo_embedding)
            texto = ""
            for z in range(0, 5):  #prepara o texto do arquivo
                try:
                    texto += sorted_we[z][0] + ";" + str(sorted_we[z][1]) + "\n"

                except:
                    print("erro")
            print(texto)
            # utils.escrever_arquivo(texto, dir_objeto + arquivo_wup_medidas)
            dic_alinhamento[sorted_we[0][0]] = palavra_bbox

        num_objeto = 0
        for palavra, value in dic_alinhamento.items():
            num_objeto += 1
            dic_json[palavra] = "Objeto " + str(num_objeto)
            x, y, w, h = bbox_objects[0].Rect()

            #draw bounding box in img_original
            cv2.rectangle(img_original, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img_original, "Objeto" + str(num_objeto), (x + 15, y + 30),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.9, (0, 255, 0), 1)

            #remove a bounding box
            bbox_objects.pop(0)
            self.lst_substantivos.remove(palavra)

        cv2.imwrite("static/" + "alinhamento2.jpg", img_original)

        #Aplica o Experimento 1
        bbox_objects = self._ordenar_bbox_tamanho(bbox_objects)
        img_original = cv2.imread("static/alinhamento2.jpg")
        texto = ""

        num_objeto = 0
        #return dic_json
        while len(bbox_objects) > 0 and len(self.lst_substantivos) > 0:
            try:
                palavra = self.lst_substantivos[0]
                #texto += entidade.palavra + "= " + str(bbox_pessoas[0].imagem) + "\n"
                num_objeto += 1

                dic_json[palavra] = "Objeto " + str(num_objeto)
                x, y, w, h = bbox_objects[0].Rect()

                #draw bounding box in img_original
                cv2.rectangle(img_original, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img_original, "Objeto" + str(num_objeto), (x + 15, y + 30),
                            cv2.FONT_HERSHEY_TRIPLEX, 0.9, (0, 255, 0), 1)

                #remove a pessoa e a bounding box
                self.lst_substantivos.pop(0)
                bbox_objects.pop(0)
            except Exception as e:
                print(e)

        cv2.imwrite("static/" + "alinhamento2.jpg", img_original)
        return dic_json
