import random
######### PLAYER CLASS ###########



class Card:

    def __init__(self, territory, symbol):
        self.territory = territory
        self.symbol = symbol

    def __str__(self):
        return self.territory + ':' + self.symbol

    @classmethod
    def wildcard(self):
        return self("WILD", "WILD")

    def print(self):
        print("Territory: ", self.territory, "Symbol: ", self.symbol)