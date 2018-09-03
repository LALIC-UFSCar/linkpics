class BoundingBox(object):

    def __init__(self, id, objeto, left, right, top, bot):
        self.id = id
        self.objeto = objeto
        self.left = left
        self.right = right
        self.top = top
        self.bot = bot
        self.width = 0
        self.height = 0
        self.centroX = 0
        self.centroY = 0
        self.area = 0
        self.CalcularTamanho()
        self.distanciaCentro = 0
        self.X = self.left
        self.Y = self.top
        self.imagem = -1
        self.label = ""
        self.lst_cnn= []

    def CalcularTamanho(self):
        self.width = self.right - self.left
        self.height = self.bot - self.top
        self.centroX = int(self.width / 2) + self.left
        self.centroY = int(self.height / 2) + self.top

    def Rect(self):
        return self.X, self.Y, self.width, self.height