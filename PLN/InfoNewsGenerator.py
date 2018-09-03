

from os import listdir
from os.path import isdir
from WordMeasure import WordMeasure
import os
import make_xls
from decimal import *


noticia_anotada= False
def file_to_List(file_name):
    lista = []
    with open(file_name, 'rt') as f:
        for line in f:
            lista.append(line.replace('\n',''))
    return lista


def dif_entidades(lst_fisicas,lst_objetos): # retorna todas as entidades presentes na lista objeto que não estão na lista entidades fisicas
    
    lst_entidades_fisicas =[]
    lst_entidades_objetos=[]
    for word_measure in lst_fisicas:
        lst_entidades_fisicas.append(word_measure.palavra)
    for word_measure in lst_objetos:
        lst_entidades_objetos.append(word_measure.palavra)
        
    lst_diferencas_entidades = [val for val in lst_entidades_objetos if val not in lst_entidades_fisicas]
    return lst_diferencas_entidades

def file_to_WordMeasure(file_measure,file_choose):
    lista_wordMeasures= []
    global noticia_anotada
    with open(file_measure, 'rt') as f:
        for line in f:
            line=line.replace('\n','') #remove caracter de quebra de linha
            valores = line.split(';') # dividir a linha em ';'
            wm= WordMeasure()
            wm.palavra = valores[0] #armazena a palavra
            TWOPLACES = Decimal(10) ** -2
            wm.valor =  Decimal(valores[1]).quantize(TWOPLACES)
            #wm.valor =  valores[1] #armazena o valor
            lista_wordMeasures.append(wm) # guarda na lista de wordMeasures
    index= 0 # serve para contar o indice das palavras
    print(file_measure+'\n')
    if not os.path.exists(file_choose): # se o arquivo não existe, coloca false em todas as palavras
        for x in range(0,len(lista_wordMeasures)):
            lista_wordMeasures[x].anotada = False
    else:
        with open(file_choose, 'rt') as f:
            for line in f:
                line=line.replace('\n','') #remove caracter de quebra de linha
                valores = line.split(';') # dividir a linha em ';'
                if len(valores[1]) > 1: # se tiver mais que um caracter, então a palavra está anotada
                    lista_wordMeasures[index].anotada = True
                    noticia_anotada= True
                index += 1
    return lista_wordMeasures

def file_to_variavel(file_name):
    texto = ""
    with open(file_name, 'rt') as f:
        for line in f:
            texto = texto + line.replace('\n', '')
    return texto


# Pega o endereço das notícias
directory_noticias= "noticias/"
#para cada noticia faça
pasta_noticias= listdir(directory_noticias) # armazena as pastas de noticias
for pasta in pasta_noticias: # para cada pasta faça
    directory_in= directory_noticias+pasta+"/"
    in_folder= listdir(directory_in) # pega o conteúdo de cada pasta
    num_pastas=0 #numero de pastas
    lista_folders_objetos= []
    for file in in_folder: #para cada arquivo faça
        if  isdir(directory_in+file):
            num_pastas = 1 + num_pastas
            if file !=  'substantivos':
                lista_folders_objetos.append(directory_in+file)
    if num_pastas > 1: # Se tem mais de uma pasta, quer dizer que há objetos, então prosseguir com essa noticia            
        noticia_anotada= False
        #------ INFORMAÇÕES DENTRO DA PASTA SUBSTANTIVOS
        lst_entidades_fisicas= file_to_List(directory_in+"substantivos/entidades_fisicas.txt") # Pega o arquivo entidades_fisicas
        lst_entidades_objetos= file_to_List(directory_in+"substantivos/entidades_objetos.txt")# Pega o arquivo entidades_objetos
        lst_entidades_interseccao= file_to_List(directory_in+"substantivos/entidades_interseccao.txt")# Pega o arquivo entidades_interseccao
        lst_entidades_diferenca= file_to_List(directory_in+"substantivos/entidades_diferenca.txt")# Pega o arquivo entidades_diferenca
        lst_entidades_nomeadas= file_to_List(directory_in+"substantivos/entidades_nomeadas.txt")# Pega o arquivo entidades nomeadas
        titulo_noticia= file_to_variavel(directory_in+"titulo.txt")
        legenda_noticia= file_to_variavel(directory_in+"caption.txt")
        #------ INFORMAÇÕES DENTRO DA PASTA DE CADA OBJETO
        dicionario_wup_fisicas= {}
        dicionario_wup_objetos= {}
        dicionario_dif_entidades_wup= {}
        dicionario_dif_entidades_embeddings= {}
        dicionario_embeddings_fisicas= {}
        dicionario_embeddings_objetos= {}
        lst_objetos= [] #lista com objetos
        lista_folders_objetos.sort()
        for objeto_file in lista_folders_objetos:        #varre a lista de folders objetos
            file_wup_distances= objeto_file+"/wup_top5_distances.txt"# Pega o arquivo wup_distances
            file_chooseWup= objeto_file+"/choose_wup.txt"# Pega o arquivo choose wup
            file_wup_distances_objects= objeto_file+"/wup_top5_distances_objects.txt"# Pega o arquivo wup_distances_objects
            file_embedding_distances= objeto_file+"/embedding_top5_distances.txt"# Pega o arquivo embedding_distances
            file_chooseEmbedding= objeto_file+"/choose_embedding.txt" # Pega o arquivo choose embeddings
            file_embedding_distances_objects= objeto_file+"/embedding_top5_distances_objects.txt" # Pega o arquivo embedding_distances_objects        
            objeto= os.path.basename(objeto_file)# Pega o nome do objeto atual
            lst_objetos.append(objeto)
            #----Monta os dicionarios ---
            #if not os.path.exists(file_chooseWup) and not os.path.exists(file_chooseEmbedding):
              #  continue
            dicionario_wup_fisicas[objeto]= file_to_WordMeasure(file_wup_distances,file_chooseWup)
            dicionario_wup_objetos[objeto]= file_to_WordMeasure(file_wup_distances_objects,'')
            dicionario_embeddings_fisicas[objeto]= file_to_WordMeasure(file_embedding_distances,file_chooseEmbedding)
            dicionario_embeddings_objetos[objeto]= file_to_WordMeasure(file_embedding_distances_objects,'')
            dicionario_dif_entidades_wup[objeto]= dif_entidades(dicionario_wup_fisicas[objeto],dicionario_wup_objetos[objeto])
            dicionario_dif_entidades_embeddings[objeto]= dif_entidades(dicionario_embeddings_fisicas[objeto],dicionario_embeddings_objetos[objeto])
        #cria o arquivo excel referente a noticia.
        make_xls.CriarArquivoXls(titulo_noticia,legenda_noticia,lst_entidades_fisicas,lst_entidades_objetos,lst_entidades_interseccao,lst_entidades_diferenca,lst_entidades_nomeadas,dicionario_wup_fisicas,dicionario_wup_objetos,dicionario_embeddings_fisicas,dicionario_embeddings_objetos,lst_objetos,file_chooseWup,file_chooseEmbedding,noticia_anotada,dicionario_dif_entidades_wup,dicionario_dif_entidades_embeddings)    
# Pega as pastas com objetos
    

