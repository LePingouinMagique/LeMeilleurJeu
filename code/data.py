#stockage des valeurs
    #pourquoi ? => création de nouvelles instange à chaque changement de map


class Data:
    def __init__(self,ui):
        self.ui = ui
        self._coins = 0
        self._health = 4
        self.max_health = 4
        self._calis = 2
        self.ui.create_hearts(self._health)

    @property
    def calis(self):
        return self._calis
    @calis.setter
    def calis(self,value):
        self._calis+= value
        self.ui.add_calice()



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