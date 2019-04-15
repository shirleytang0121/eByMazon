from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty,StringProperty
from kivy.core.window import Window

userID = -1
itemID = -1

class LoginScreen(Screen):
    def checkLogin(self,username,password):
        print("Username: %s \nPassword: %s" % (username,password))
        global userID
        userID = 0


class signUp(Screen):
    def checkSignUp(self, firstName, lastName, email, username):
        print("First Name: %s \n Last Name %s Email %s Username %s" % (firstName, lastName, email, username))

class HomePage(Screen):

    def searchKeyword(self, word):
        print(word)
        print(userID)

    def sort_feature(self,feature):
        print(feature)


class ScreenManagement(ScreenManager):
    # userID = StringProperty("-1")
    # itemID = StringProperty("-1")
    pass




class MainApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return Builder.load_file("project.kv")


if __name__ == "__main__":
    MainApp().run()