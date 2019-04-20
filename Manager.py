import mysql.connector
from mysql.connector import errorcode, OperationalError

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.core.window import Window


from GeneralFunctions import General
from GU import GU
from SU import SU
from OU import OU
from Item import Item
from otherClass import *


class Manager(Screen):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.displayItem()

    def sortPop(self):
        print("Sort by Popular")
    def sortRating(self):
        print("Sort by Rating")
    def sortPricelh(self):
        print("Sort by price low to high")
    def sortPricehl(self):
        print("Sort by price high to low")



    def displayItem(self):
        self.ids['rv'].data = general.popularItem()
            # [{'value': "Button " + str(x), 'cool': str(x)} for x in range(3)]

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



    def checkLogin(self,username,password):
        print("Username: %s \nPassword: %s" % (username,password))
        userInfo = general.login_check(username,password)
        if userInfo:
            self.login = True
            self.ids['screenmanager'].current = "homepage"
            self.ids['loginCheck'].text = ""
        else:
            self.login = False
            self.ids['loginCheck'].text ="Login Info Not Correct"


    def signUp(self,username, name, phone, email,address,state,card):
        applied = guest.apply(username, name, email,card,address,state,phone)
        if applied:
            self.ids['userRepeat'].text = ""
            self.ids['screenmanager'].current = "homepage"
        else:
            self.ids['userRepeat'].text = "Fail to Apply!!!"



    def checkUsername(self, username):
        nameCheck = guest.checkUsername(username)
        if not nameCheck:
            self.ids['userRepeat'].text = "Username already Existed!!!"
        else:
            self.ids['userRepeat'].text = "Username can be used "


    def searchKeyword(self, word):
        self.displayItem()
        print(word)




    def friendlist(self):
        print('friendlist')

    # def history(self):
    #     print('history')

class eByMazonApp(App):

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Builder.load_file("manage.kv")
        root = Manager()
        return root

if __name__ == "__main__":
    config = {
        "user": '',                 # Enter your own username
        "password": '',             # Enter your own password
        "host": '127.0.0.1',
        "database": 'eByMazon'
    }

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(buffered=True)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        raise err

    general = General(cursor=cursor)
    guest = GU(cursor=cursor)
    eByMazonApp().run()