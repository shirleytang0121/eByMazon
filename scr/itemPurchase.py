from kivy.uix.screenmanager import Screen
# self define classes
try:
    from scr.GeneralFunctions import General
    from scr.GU import GU
    from scr.SU import SU
    from scr.OU import OU
    from scr.Item import Item
    # from scr.otherClass import *
except ModuleNotFoundError:
    from GeneralFunctions import General
    from GU import GU
    from SU import SU
    from OU import OU
    from Item import Item
    # from otherClass import *

class FixedPurchase(Screen):
    def clear(self):
        self.singlePrice = 0
        self.numberBuy = 0
        self.tax = 0
        self.vip = 0
        self.friend = 0
        self.finalPrice =0
        self.purchased = False

    def infoLoad(self, item, ou, numWant):
        self.singlePrice = item.price
        self.numberBuy = numWant
        total = self.singlePrice*self.numberBuy
        self.tax = round(ou.taxRate*total,3)
        self.vip = 0.05* total if ou.status == 1 else 0
        self.friend =0
        self.finalPrice = 0

    def purchasing(self):
        self.purchased = True
        self.ids["purchaseManager"].current = "empty"