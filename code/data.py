#stockage des valeurs
    #pourquoi ? => création de nouvelles instange à chaque changement de map


class Data:
    def __init__(self,ui):
        self.ui = ui
        self._coins = 0
        self._health = 4
        self.ui.create_hearts(self._health)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self,value):
        self._health = value
        self.ui.create_hearts(value)

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self,amount):

        self._coins = amount
        self.ui.show_coin(amount)