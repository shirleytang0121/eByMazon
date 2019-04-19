from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty,StringProperty
from kivy.core.window import Window


class ImageButton(Screen):
    pass


class Comment(Screen):
    pass

class PurchaseButton(Screen):
    pass

class BiddingButton(Screen):
    pass

class PurchasePage(Screen):
    pass
    
class Purchase(ScreenManager):
    pass



class MainApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return Builder.load_file("item_purchase1.kv")


if __name__ == "__main__":
    MainApp().run()