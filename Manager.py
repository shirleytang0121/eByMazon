from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window

class Home(Screen):

    ttext = 'Screen 2'
    #other code

class Login(Screen):
    def setText(self):
        self.ids['button1'].text="Now"
        self.ids['screenmanager'].current ="testy_screen"
    pass

class Signup(Screen):
    # def checkUsername(self, username):
    #     # self.ids['userRepeat'].text = "Username already "
    #     self.ids['show'] = True
    #     print("SU username : %s"% username)
    #
    #     pass
    pass

class OUprofile(Screen):
    pass

class FriendList(Screen):
    pass

class History(Screen):
    pass
class EditProfile(Screen):
    pass

class Manager(Screen):

    def tohome(self):
        self.ids['screenmanager'].current = "homepage"
    def tologin(self):
        self.ids['screenmanager'].current = "loginpage"
    def signup(self):
        self.ids['screenmanager'].current = "signupPage"
    def toProfile(self):
        self.ids['screenmanager'].current = "profilePage"


    def editInfo(self):
        self.ids['screenmanager'].current = "editPage"
    def friendLst(self):
        self.ids['screenmanager'].current = "friendPage"
    def history(self):
        self.ids['screenmanager'].current = "historyPage"
    def setText(self):
        print("In")
        self.ids['button1'].text="Now"
        self.ids['screenmanager'].current ="testy_screen"
    pass

    # def checkUsername(self, username):
    #     print("username : %s"% username)
    #     pass

    def checkLogin(self,username,password):
        print("Username: %s \nPassword: %s" % (username,password))
        self.ids['screenmanager'].current = "homepage"


    def checkSignUp(self,firstName, lastName, email,username):
        self.ids['screenmanager'].current = "homepage"


    def checkUsername(self, username):
        # self.ids['userRepeat'].text = "Username already "
        self.ids['userRepeat'].text = "Username already Existed"
        print("SU username : %s"% username)

        pass



    def searchKeyword(self, word):
        print(word)


    def sort_feature(self,feature):
        print(feature)

    def friendlist(self):
        print('friendlist')

    # def history(self):
    #     print('history')

class ShowcaseApp(App):

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Builder.load_file("main.kv")
        root = Manager()
        return root

if __name__ == "__main__":
    ShowcaseApp().run()