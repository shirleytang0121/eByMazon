from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
class Home(Screen):
    # For radio buttons
    blue = ObjectProperty(True)
    red = ObjectProperty(False)
    green = ObjectProperty(False)

    pass


class Login(Screen):
    # def setText(self):
    #     self.ids['button1'].text="Now"
    #     self.ids['screenmanager'].current ="testy_screen"
    pass

class Signup(Screen):
    # def get(self):
    #     print(self.ids['userRepeat'].text)
    #     return self.ids['userRepeat'].text
    # def checkUsername(self, username):
    #     # self.ids['userRepeat'].text = "Username already "
    #     self.ids['show'] = True
    #     print("SU username : %s"% username)
    #
    #     pass
    pass

class suHomepage(Screen):
    pass
class Item(Screen):
    pass
class OUprofile(Screen):
    pass

class FriendList(Screen):
    pass

class History(Screen):
    pass
class EditProfile(Screen):
    pass