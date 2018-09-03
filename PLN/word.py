class Palavra(object):
    def __init__(self, id,palavra, classe_morfo,lema, entidade_nomeada,anterior,posterior,ocorrencias,num_documentos,total_palavras_documentos,presente_legenda,presente_titulo,indice):
      self.id = id
      self.palavra =palavra
      self.classe_morfo= classe_morfo
      self.lema= lema
      self.entidade_nomeada=entidade_nomeada
      self.anterior=anterior
      self.posterior=posterior
      self.ocorrencias= ocorrencias
      self.numero_documentos= num_documentos
      self.total_palavras_documentos = total_palavras_documentos
      self.presente_legenda= presente_legenda
      self.presente_titulo = presente_titulo
      self.indice_treetagger=  indice
      self.palavra_completa= palavra
      self.segundo_nome= ""
      self.terceiro_nome=""

class Palavra_original(object):
    def __init__(self,id,palavra):
        self.id= id
        self.palavra = palavra