
from kivy.uix.screenmanager import Screen



# Used to display popup
class LoginScreen(Screen):

    def checkLogin(self,username,password):
        print("Username: %s \nPassword: %s" % (username,password))
        LoginScreen.dismiss(self)
class NewUser(Popup):
    pass