from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
# from kivy.properties import ObjectProperty,StringProperty
from kivy.core.window import Window

userID = -1
itemID = -1

class LoginScreen(Screen):
    def checkLogin(self,username,password):
        print("Username: %s \nPassword: %s" % (username,password))
        global userID
        userID = 0


class NewUser(Screen):
    pass

class HomePage(Screen):

    def searchKeyword(self, word):
        print(word)
        print(userID)

    def sort_feature(self,feature):
        print(feature)


class OSprofile(Screen):

    def friendlist(self):
        print()
    
    def history(self):
        print()
    

class FriendList(Screen):
    pass

class History(Screen):
    pass

class EditProfile(Screen):
    pass

    


class ScreenManagement(ScreenManager):
    # userID = StringProperty("-1")
    # itemID = StringProperty("-1")
    pass





class MainApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return Builder.load_file("manage.kv")


if __name__ == "__main__":
    MainApp().run()