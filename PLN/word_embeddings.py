import os
import sys
import numpy as np
import operator


class WordEmbeding(object):
    def __init__(self, tam):
        self.EMBEDDING_DIM = tam
        self.GLOVE_DIR = "/data/alinhador/"

    # Carrega todos os WordEmbeddings em um dictonary contendo->{palavra,vetor}
    def CarregarWordEmbeddings(self):
        print('Indexing word vectors.')

        f = open(os.path.join(self.GLOVE_DIR, 'glove.6B.100d.txt'))
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs

        f.close()

        print('Found %s word vectors.' % len(embeddings_index))

    def RetornarTamanhoEmbedding(self):
        return len(embeddings_index)

    def RetornarVetor(self, palavra):
        for word, vec in embeddings_index.items():
            if word == palavra:  # se encontrar a palavra
                return vec  # retorna o vetor

    def RetornarDicionario(self, lst_substantivos):  #recebe a lista de substantivos ordenados alfabeticamente
        embeddings_substantivos = {}

        for palavra in lst_substantivos:

            for word, vec in embeddings_index.items():
                if word == palavra:  # se encontrar a palavra
                    embeddings_substantivos[word] = vec  # retorna o vetor
        return embeddings_substantivos


embeddings_index = {}
