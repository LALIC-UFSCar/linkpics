import os
from .boundingBox import BoundingBox
#from IA.classificadores.classify_image import CnnClassifier
from PIL import Image
import math
import cv2
#from classify_image import CnnClassifier
import subprocess


class Imagem(object):
    def __init__(self, path_imagem, path_dir, path_projeto):
        self.path_projeto = path_projeto
        self.path = path_projeto + path_imagem
        self.width = 0
        self.height = 0
        self.centroX = 0
        self.centroY = 0
        self.GetImageSize()
        self.CalcularCentro()
        self.list_boundingBox = []
        self.list_boundingBox9000 = []
        self.list_boundingBoxOrganizada = []
        self.list_boundingBoxOrganizada_9000 = []
        self.numero_pessoas = 0
        self.path_diretorio = path_projeto + path_dir
        print("dentro do construtor")
       # self.classificadorCNN = CnnClassifier("resnet")
        #self.classificador= CnnClassifier("resnet")

    def renomearArquivos(self):
        os.rename(self.path_projeto + "noticia_atual/image_result.txt", self.path_diretorio + "/image_result.txt")
        print("removido")

    # os.rename("noticia_atual/extraction_result.txt", self.path_diretorio + "/extraction_result.txt")
    # os.rename("noticia_atual/darknet_result.txt", self.path_diretorio + "/darknet_result.txt")

    def aplicarYolo(self):
        try:
            os.remove("predictions.png")  # tenta apagar o arquivo "predictions.png"
        except OSError:
            pass
        try:
            # os.system("./darknet detect cfg/yolo.cfg weights/yolo.weights " + self.path + ">> noticia_atual/image_result.txt")  # aplica a deteccao YOLO
            #p = subprocess.Popen(["./darknet","detect","cfg/yolo.cfg","weights/yolo.weights",self.path,">>","noticia_atual/image_result.txt"])
            with open(self.path_projeto + "noticia_atual/image_result.txt", "wb") as out:
                p = subprocess.Popen(
                    ["./darknet", "detect", "cfg/yolo.cfg", "/data/alinhador/yolo.weights", self.path,"-thresh","0.4"],
                    cwd=self.path_projeto + "IA/YOLO",
                    stdout=out)
                p.wait()
        except OSError as e:
            print('erro aqui')
            print(str(e))
            pass
        if os.path.exists(self.path_projeto + "IA/YOLO/predictions.png"):
            os.rename(
                self.path_projeto + "IA/YOLO/predictions.png",
                self.path_diretorio + "/img_yolo.png")  # renomeia a imagem yolo e passa para o diretorio da noticia

    

    def aplicarEXTRACTION(self, img_path):
        try:

            with open(self.path_projeto + "noticia_atual/extraction_result.txt", "wb") as out:
                p = subprocess.Popen(
                    ["./darknet", "classifier","predict", "cfg/imagenet1k.data","cfg/extraction.cfg", "/data/alinhador/extraction.weights",  self.path_projeto+img_path],
                    cwd=self.path_projeto + "IA/YOLO",
                    stdout=out)
                p.wait()
        except OSError as e:
                print(str(e))
                pass

    def aplicarDARKNET(self, img_path):        
        try:

            with open(self.path_projeto + "noticia_atual/darknet_result.txt", "wb") as out:
                p = subprocess.Popen(
                    ["./darknet", "classifier","predict", "cfg/imagenet1k.data","cfg/darknet19.cfg", "/data/alinhador/darknet19.weights",  self.path_projeto+img_path],
                    cwd=self.path_projeto + "IA/YOLO",
                    stdout=out)
                p.wait()
        except OSError as e:
                print(str(e))
                pass

    def aplicarResNet50(self, img_path):        
        try:

            with open(self.path_projeto + "noticia_atual/resnet_50_result.txt", "wb") as out:
                p = subprocess.Popen(
                    ["./darknet", "classifier","predict", "cfg/imagenet1k.data","cfg/resnet50.cfg", "/data/alinhador/resnet50.weights",  self.path_projeto+img_path],
                    cwd=self.path_projeto + "IA/YOLO",
                    stdout=out)
                p.wait()
        except OSError as e:
                print(str(e))
                pass       


    def aplicarDenseNet(self, img_path):        
        try:

            with open(self.path_projeto + "noticia_atual/densenet_201_result.txt", "wb") as out:
                p = subprocess.Popen(
                    ["./darknet", "classifier","predict", "cfg/imagenet1k.data","cfg/densenet201.cfg", "/data/alinhador/densenet201.weights",  self.path_projeto+img_path],
                    cwd=self.path_projeto + "IA/YOLO",
                    stdout=out)
                p.wait()
        except OSError as e:
                print(str(e))
                pass           


    def aplicarVgg16(self, img_path):        
     
        try:

            with open(self.path_projeto + "noticia_atual/vgg_16_result.txt", "wb") as out:
                print("ENTROU AQUI")
                p = subprocess.Popen(
                    ["./darknet", "classifier","predict", "cfg/imagenet1k.data","cfg/vgg-16.cfg", "/data/alinhador/vgg-16.weights",  self.path_projeto+img_path],
                    cwd=self.path_projeto + "IA/YOLO",
                    stdout=out)
                p.wait()
        except OSError as e:
                print(str(e))
                pass    


    def read_words(self):
        #arquivo_txt= "noticia_atual/image_result.txt"
        arquivo_txt = self.path_diretorio + "/image_result.txt"
        open_file = open(arquivo_txt, 'r')
        words_list = []
        contents = open_file.readlines()
        return contents

    def read_wordsYolo9000(self):
        arquivo_txt = "noticia_atual/image_result9000.txt"
        open_file = open(arquivo_txt, 'r')
        words_list = []
        contents = open_file.readlines()
        return contents

    def read_wordsDarkNet(self):
        arquivo_txt = "noticia_atual/darknet_result.txt"
        open_file = open(arquivo_txt, 'r')
        words_list = []
        contents = open_file.readlines()
        return contents

    def read_wordsExtraction(self):
        arquivo_txt = "noticia_atual/extraction_result.txt"
        open_file = open(arquivo_txt, 'r')
        words_list = []
        contents = open_file.readlines()
        return contents

    def read_wordsDenseNet(self):
        arquivo_txt = "noticia_atual/densenet_201_result.txt"
        open_file = open(arquivo_txt, 'r')
        words_list = []
        contents = open_file.readlines()
        return contents

    def read_wordsDenseNet(self):
        arquivo_txt = "noticia_atual/densenet_201_result.txt"
        open_file = open(arquivo_txt, 'r')
        words_list = []
        contents = open_file.readlines()
        return contents

    def ClassificarBoundingBox(self):

        img_original = cv2.imread(self.path_diretorio + "/img_original.jpg", 1)
        for bBox in self.list_boundingBoxOrganizada:  # para cada bounding box
            if bBox.objeto != "person":  # se a bBox não for pessoa faça
                new_sample = img_original.copy()
                crop = new_sample[bBox.top:bBox.bot, bBox.left:bBox.right]
                cv2.imwrite("bBoxImage.png", crop)
                # top_resnet = self.classificadorCNN.classifyImage("bBoxImage.png", self.path_diretorio, bBox.objeto)
                # print(top_resnet)
                self.aplicarDARKNET("bBoxImage.png")
                top_darknet = self.ObterTop5Darknet()
                self.aplicarEXTRACTION("bBoxImage.png")
                top_extraction = self.ObterTop5Extraction()
                #self.aplicarResNet50("bBoxImage.png")           
                self.aplicarDenseNet("bBoxImage.png")
                top_dense_net = self.ObterTop5DenseNet()
                self.aplicarVgg16("bBoxImage.png")
                print("APLICADO DARKNET - EXTRACTION - DENSE_NET")
                print(top_darknet)
                print(top_extraction)
                print(top_dense_net)
                lst_cnn = []
                lst_cnn = list(set().union(top_darknet,top_extraction, top_dense_net))
                print(lst_cnn)
                bBox.lst_cnn = lst_cnn
                                                        

    def ObterBoundingBox(self):
        self.renomearArquivos()
        arquivo_informacoes_boundingBox = self.read_words()  # le as informações geradas pela YOLO
        informacoes_bounding = []

        for i in range(len(arquivo_informacoes_boundingBox)):
            if i != 0:
                informacoes_bounding = arquivo_informacoes_boundingBox[i].split(
                    ',')  #pega as informações da linha e quebra em pedaços
                # Preenche a classe bounding box com as informações obtidas
                objeto = informacoes_bounding[0]
                if objeto != "tie":
                    left = int(informacoes_bounding[1])
                    right = int(informacoes_bounding[2])
                    top = int(informacoes_bounding[3])
                    bot = int(informacoes_bounding[4])
                    b_box = BoundingBox(i, objeto, left, right, top, bot)
                    # print(str(b_box.centroX)+"-"+str(b_box.centroY))
                    self.list_boundingBox.append(b_box)

    #  print("" + str(len(list_boundingBox)));

    def ObterBoundingBox9000(self):
        arquivo_informacoes_boundingBox = self.read_wordsYolo9000()  # le as informações geradas pela YOLO
        informacoes_bounding = []

        for i in range(len(arquivo_informacoes_boundingBox)):
            if i != 0:
                informacoes_bounding = arquivo_informacoes_boundingBox[i].split(
                    ',')  # pega as informações da linha e quebra em pedaços
                # Preenche a classe bounding box com as informações obtidas
                objeto = informacoes_bounding[0]
                left = int(informacoes_bounding[1])
                right = int(informacoes_bounding[2])
                top = int(informacoes_bounding[3])
                bot = int(informacoes_bounding[4])
                b_box = BoundingBox(i, objeto, left, right, top, bot)
                # print(str(b_box.centroX)+"-"+str(b_box.centroY))
                self.list_boundingBox9000.append(b_box)
                #  print("" + str(len(list_boundingBox)));

    def ObterTop5Darknet(self):
        lst_darknet_words = []
        arquivo_informacoes_darknet = self.read_wordsDarkNet()  # le as informações geradas pela YOLO
        informacoes_bounding = []

        for i in range(len(arquivo_informacoes_darknet)):
            if i > 1:
                informacoes_bounding = arquivo_informacoes_darknet[i].split(
                    ':')  # pega as informações da linha e quebra em pedaços
                # Preenche o list de palavras da darknet
                lst_palavra = informacoes_bounding[0].split(" ")
                palavra = ''
                if len(lst_palavra) > 1:
                    palavra = lst_palavra[1]
                else:
                   palavra = lst_palavra[0] 
                lst_darknet_words.append(palavra)
        print('palavras dark net')
        print(lst_darknet_words)
        return lst_darknet_words  #devolve o list de palavras

    
    
    
    def ObterTop5Extraction(self):
        lst_extraction_words = []
        arquivo_informacoes_extraction = self.read_wordsExtraction()  # le as informações geradas pela YOLO
        informacoes_bounding = []

        for i in range(len(arquivo_informacoes_extraction)):
            if i > 1:
                informacoes_bounding = arquivo_informacoes_extraction[i].split(
                    ':')  # pega as informações da linha e quebra em pedaços
                # Preenche o list de palavras da darknet
                lst_palavra = informacoes_bounding[0].split(" ")
                palavra = ''
                if len(lst_palavra) > 1:
                    palavra = lst_palavra[1]
                else:
                   palavra = lst_palavra[0] 
                lst_extraction_words.append(palavra)
        print('palavras extraction net')
        print(lst_extraction_words)
        return lst_extraction_words  # devolve o list de palavras
    
    def ObterTop5DenseNet(self):
        lst_dense_net_words = []
        arquivo_informacoes_dense_net = self.read_wordsDenseNet()  # le as informações geradas pela YOLO
        informacoes_bounding = []
        
        for i in range(len(arquivo_informacoes_dense_net)):
            if i > 1:
                informacoes_bounding = arquivo_informacoes_dense_net[i].split(
                    ':')  # pega as informações da linha e quebra em pedaços
                # Preenche o list de palavras da darknet
                lst_palavra = informacoes_bounding[0].split(" ")
                palavra = ''
                if len(lst_palavra) > 1:
                    palavra = lst_palavra[1]
                else:
                   palavra = lst_palavra[0] 
                lst_dense_net_words.append(palavra)
        print('palavras dense net')
        print(lst_dense_net_words)
        return lst_dense_net_words  # devolve o list de palavras

    def GetImageSize(self):
        print(self.path)
        with Image.open(self.path) as im:
            w, h = im.size
            self.width = w
            self.height = h

    def CalcularCentro(self):
        self.centroX = int(self.width / 2)
        self.centroY = int(self.height / 2)

    def OrganizarBoundingBoxes(self):
        numero_repeticoes = len(self.list_boundingBox)  # pega o total de bounding box
        count = 0
        while count < numero_repeticoes:
            menor_distancia = 10000
            indice_menor_distancia = -1          
            total_bounding = len(self.list_boundingBox)  # total de bounding box restantes
            
            for i in range(0, total_bounding):
                distancia = self.CalcularDistancia(self.centroX, self.height, self.list_boundingBox[i].centroX,
                                                   self.list_boundingBox[i].centroY)
                if distancia < menor_distancia:
                    menor_distancia = distancia  #guarda a menor distancia
                    indice_menor_distancia = i  #guarda o indice da menor distancia
            
            self.list_boundingBox[indice_menor_distancia].distanciaCentro = menor_distancia
            
            self.list_boundingBoxOrganizada.append(
                self.list_boundingBox[indice_menor_distancia])  # coloca na lista o Bounding box de menor distancia
            self.list_boundingBoxOrganizada[count].imagem = count
            self.list_boundingBox.remove(self.list_boundingBox[indice_menor_distancia])
            count = count + 1

    def OrganizarBoundingBoxes9000(self):
        numero_repeticoes = len(self.list_boundingBox9000)  # pega o total de bounding box
        count = 0
        while count < numero_repeticoes:
            menor_distancia = 10000
            indice_menor_distancia = -1
            total_bounding = len(self.list_boundingBox9000)  # total de bounding box restantes
            for i in range(0, total_bounding):
                distancia = self.CalcularDistancia(self.centroX, self.height, self.list_boundingBox9000[i].centroX,
                                                   self.list_boundingBox9000[i].centroY)
                if distancia < menor_distancia:
                    menor_distancia = distancia  #guarda a menor distancia
                    indice_menor_distancia = i  #guarda o indice da menor distancia
            self.list_boundingBox9000[indice_menor_distancia].distanciaCentro = menor_distancia
            self.list_boundingBoxOrganizada_9000.append(
                self.list_boundingBox9000[indice_menor_distancia])  # coloca na lista o Bounding box de menor distancia
            self.list_boundingBoxOrganizada_9000[count].imagem = count + 20
            self.list_boundingBox9000.remove(self.list_boundingBox9000[indice_menor_distancia])
            count = count + 1

    def BoundingBoxApproach(self):  # remove as bounding box que estão dentro de outras Bbox

        finalizou = 0
        while finalizou == 0:  #  nao terminou ainda
            finalizou = 1
            total_bounding = len(self.list_boundingBoxOrganizada)  # total de bounding box
            for i in range(0, total_bounding):  #para cada bBox faça
                if finalizou == 0:
                    break
                if i == 0:  #pula a primeira que é a mais bem classificada
                    continue
                else:  # a partir das outras faça

                    if self.list_boundingBoxOrganizada[i].objeto == "person":
                        area_atual = self.list_boundingBoxOrganizada[i].width * self.list_boundingBoxOrganizada[
                            i].height
                        eixoXatual_ini = self.list_boundingBoxOrganizada[i].left
                        eixoXatual_fim = self.list_boundingBoxOrganizada[i].right
                        eixoYatual_ini = self.list_boundingBoxOrganizada[i].top
                        eixoYatual_fim = self.list_boundingBoxOrganizada[i].bot
                        lst_intervalo_atual_width = self.PreencherListaIntervalos(eixoXatual_ini, eixoXatual_fim)
                        lst_intervalo_atual_height = self.PreencherListaIntervalos(eixoYatual_ini, eixoYatual_fim)
                        for x in range(
                                0, i):  # varre todas as bounding box anteriores para saber se a atual está dentro delas
                            if self.list_boundingBoxOrganizada[x].objeto == "person":
                                # eixo ALVO
                                eixoXalvo_ini = self.list_boundingBoxOrganizada[x].left
                                eixoXalvo_fim = self.list_boundingBoxOrganizada[x].right
                                eixoYalvo_ini = self.list_boundingBoxOrganizada[x].top
                                eixoYalvo_fim = self.list_boundingBoxOrganizada[x].bot
                                area_alvo = self.list_boundingBoxOrganizada[x].width * self.list_boundingBoxOrganizada[
                                    x].height
                                lst_intervalo_alvo_width = self.PreencherListaIntervalos(eixoXalvo_ini, eixoXalvo_fim)
                                lst_intervalo_alvo_height = self.PreencherListaIntervalos(eixoYalvo_ini, eixoYalvo_fim)
                                # calcula qual o range que as bounding box se encontram
                                lst_width = self.intersect(lst_intervalo_atual_width, lst_intervalo_alvo_width)
                                lst_height = self.intersect(lst_intervalo_atual_height, lst_intervalo_alvo_height)
                                width_interseccao = 0
                                height_inserseccao = 0
                                if len(lst_width) >= 2:
                                    width_interseccao = lst_width[len(lst_width) - 1] - lst_width[0]
                                if len(lst_height) >= 2:
                                    height_inserseccao = lst_height[len(lst_height) - 1] - lst_height[0]
                                area_interseccao = width_interseccao * height_inserseccao
                                if area_interseccao >= (area_alvo * 0.25):
                                    self.list_boundingBoxOrganizada.remove(self.list_boundingBoxOrganizada[i])
                                    finalizou = 0
                                    break

    def BoundingBoxApproach9000(self):  # remove as bounding box que estão dentro de outras Bbox

        finalizou = 0
        while finalizou == 0:  # nao terminou ainda
            finalizou = 1
            total_bounding = len(self.list_boundingBoxOrganizada_9000)  # total de bounding box
            for i in range(0, total_bounding):  # para cada bBox faça
                if finalizou == 0:
                    break
                if i == 0:  # pula a primeira que é a mais bem classificada
                    continue
                else:  # a partir das outras faça

                    if self.list_boundingBoxOrganizada_9000[i].objeto == "person":
                        area_atual = self.list_boundingBoxOrganizada_9000[
                            i].width * self.list_boundingBoxOrganizada_9000[i].height
                        eixoXatual_ini = self.list_boundingBoxOrganizada_9000[i].left
                        eixoXatual_fim = self.list_boundingBoxOrganizada_9000[i].right
                        eixoYatual_ini = self.list_boundingBoxOrganizada_9000[i].top
                        eixoYatual_fim = self.list_boundingBoxOrganizada_9000[i].bot
                        lst_intervalo_atual_width = self.PreencherListaIntervalos(eixoXatual_ini, eixoXatual_fim)
                        lst_intervalo_atual_height = self.PreencherListaIntervalos(eixoYatual_ini, eixoYatual_fim)
                        for x in range(
                                0, i):  # varre todas as bounding box anteriores para saber se a atual está dentro delas
                            if self.list_boundingBoxOrganizada_9000[x].objeto == "person":
                                # eixo ALVO
                                eixoXalvo_ini = self.list_boundingBoxOrganizada_9000[x].left
                                eixoXalvo_fim = self.list_boundingBoxOrganizada_9000[x].right
                                eixoYalvo_ini = self.list_boundingBoxOrganizada_9000[x].top
                                eixoYalvo_fim = self.list_boundingBoxOrganizada_9000[x].bot
                                area_alvo = self.list_boundingBoxOrganizada_9000[
                                    x].width * self.list_boundingBoxOrganizada_9000[x].height
                                lst_intervalo_alvo_width = self.PreencherListaIntervalos(eixoXalvo_ini, eixoXalvo_fim)
                                lst_intervalo_alvo_height = self.PreencherListaIntervalos(eixoYalvo_ini, eixoYalvo_fim)
                                # calcula qual o range que as bounding box se encontram
                                lst_width = self.intersect(lst_intervalo_atual_width, lst_intervalo_alvo_width)
                                lst_height = self.intersect(lst_intervalo_atual_height, lst_intervalo_alvo_height)
                                width_interseccao = 0
                                height_inserseccao = 0
                                if len(lst_width) >= 2:
                                    width_interseccao = lst_width[len(lst_width) - 1] - lst_width[0]
                                if len(lst_height) >= 2:
                                    height_inserseccao = lst_height[len(lst_height) - 1] - lst_height[0]
                                area_interseccao = width_interseccao * height_inserseccao
                                if area_interseccao >= (area_alvo * 0.25):
                                    self.list_boundingBoxOrganizada_9000.remove(self.list_boundingBoxOrganizada_9000[i])
                                    finalizou = 0
                                    break

    def PreencherListaIntervalos(self, ini, fim):
        lst_intervalo = []
        for valor in range(ini, fim):
            lst_intervalo.append(valor)
        return lst_intervalo

    def intersect(self, a, b):
        return list(set(a) & set(b))

    def CalcularDistancia(self, x_imagem, y_imagem, x_boundingBox, y_boundingBox):
        distancia = math.sqrt((math.pow(x_imagem - x_boundingBox, 2)) +
                              (math.pow(y_imagem - y_boundingBox, 2)))  # calcula distancia euclidiana
        return distancia

    def GerarFotos(self):  # função que gera uma nova imagem para cada bounding_box
        for i in range(0, len(self.list_boundingBoxOrganizada)):  # para cada uma , pinte a bounding box
            image = cv2.imread(self.path)  #carrega a imagem original
            x = self.list_boundingBoxOrganizada[i].left
            y = self.list_boundingBoxOrganizada[i].top
            w = self.list_boundingBoxOrganizada[i].width
            h = self.list_boundingBoxOrganizada[i].height
            try:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                #cv2.line(image, (self.list_boundingBoxOrganizada[i].centroX,  self.list_boundingBoxOrganizada[i].centroY), (self.centroX, self.height), (255, 255, 255), 6)
                #  cv2.imshow("result",image)
                cv2.imwrite(self.path_diretorio + "/" + str(i) + ".jpg", image)
            #  cv2.waitKey()
            except:
                print("erro")

    def GerarFotos9000(self):  # função que gera uma nova imagem para cada bounding_box
        for i in range(0, len(self.list_boundingBoxOrganizada_9000)):  # para cada uma , pinte a bounding box
            image = cv2.imread(self.path)  # carrega a imagem original
            x = self.list_boundingBoxOrganizada_9000[i].left
            y = self.list_boundingBoxOrganizada_9000[i].top
            w = self.list_boundingBoxOrganizada_9000[i].width
            h = self.list_boundingBoxOrganizada_9000[i].height
            try:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # cv2.line(image, (self.list_boundingBoxOrganizada[i].centroX,  self.list_boundingBoxOrganizada[i].centroY), (self.centroX, self.height), (255, 255, 255), 6)
                #  cv2.imshow("result",image)
                num_image = 20 + i
                cv2.imwrite("noticia_atual/" + str(num_image) + ".jpg", image)
                #  cv2.waitKey()
            except:
                print("erro")

    def ContarPessoas(self):
        count = 0
        total_bounding = len(self.list_boundingBox)  # total de bounding box
        for i in range(0, total_bounding):  # para cada bouding box procurar numero de pessoas
            if self.list_boundingBox[i].objeto == "person":
                count = count + 1
        self.numero_pessoas = count
        return count

    def retornar_bbox_pessoa(self):
        """ Retorna as Bounding Box contendo pessoas """
        lst_pessoas = []
        total_bounding = len(self.list_boundingBoxOrganizada)  # total de bounding box
        for i in range(0, total_bounding):  # para cada bouding box procurar numero de pessoas
            if self.list_boundingBoxOrganizada[i].objeto == "person":
                lst_pessoas.append(self.list_boundingBoxOrganizada[i])

        return lst_pessoas