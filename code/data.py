#stockage des valeurs
    #pourquoi ? => création de nouvelles instange à chaque changement de map


class Data:
    def __init__(self,ui):
        self.ui = ui
        self.coins = 0
        self._health = 10

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self,value):
        self._health = value
        self.ui.create_hearts(value)