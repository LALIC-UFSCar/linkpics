import threading


class ThreadPLN(threading.Thread):
    """Classe que executa a thread de processamento do texto"""

    def __init__(self, threadID, name, pln):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.pln = pln

    def run(self):
        print("Starting " + self.name)
        self.pln.FiltrarTexto()
        self.pln.ObterPalavrasLegenda()
        self.pln.ObterPalavrasTitulo()
        self.pln.AplicarTreeTagger()
        self.pln.entidades_legenda()
        # pln.AplicarStanforNER()
        # pega os substantivos que estejam com physical entity na wordnet
        self.pln.ObterEntidadesNomeadas_SubstantivosValidos('physical_entity.n.01')
        #---- Pega as entidades mais importantes do texto
        self.pln.OrganizarTopEntidadesNomeadas()
        #----- Pega os substantivos mais importantes do texto
        self.pln.OrganizarTopSubstantivos()
        # pega os substantivos que estejam com object na wordnet
        self.pln.ObterEntidadesNomeadas_SubstantivosValidos('object.n.01')
        #----- Pega os substantivos mais importantes do texto
        self.pln.OrganizarTopSubstantivos()
        #self.pln.InterseccaoListasSubstantivos()  #Interseccao dos objetos
        #self.pln.DiferencaListasSubstantivos()
        print("---Salvando Lista de substantivos---")
        self.pln.SalvarListasSubstantivos()
        # print("str(len(pln.lst_diferenca_entidades))")
        print("Exiting " + self.name)
