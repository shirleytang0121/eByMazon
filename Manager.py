import mysql.connector
from mysql.connector import errorcode, OperationalError

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window

from GeneralFunctions import General
from GU import GU
from SU import SU
from OU import OU
from Item import Item





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

def convert_data(data):
    l = []
    for item in data:
        for key, value in item.items():
            l.append({'text': key, 'value': value})
    return l

class Manager(Screen):
    def abc(self):
        #fetching from database
        arr = ({'Item1': 5000},{'Item2': 1000},{'Item 3':500})

        # convert to [{'text': 'Item1', 'value': 5000}, {'text': 'Item2', 'value': 1000}]
        self.ids['rv'].data = convert_data(arr)
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
        userInfo = general.login_check(username,password)
        if userInfo:
            self.login = True
            self.ids['screenmanager'].current = "homepage"
        else:
            self.login = False


    def signUp(self,username, name, phone, email,address,state,card):
        applied = guest.apply(username, name, email,card,address,state,phone)
        if applied:
            self.ids['userRepeat'].text = ""
            self.ids['screenmanager'].current = "homepage"
        else:
            self.ids['userRepeat'].text = "Fail to Apply"



    def checkUsername(self, username):
        nameCheck = guest.checkUsername(username)
        if not nameCheck:
            self.ids['userRepeat'].text = "Username already Existed"
        else:
            self.ids['userRepeat'].text = "Username can be used "




    def searchKeyword(self, word):
        self.abc()
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
        Builder.load_file("manage.kv")
        root = Manager()
        return root

if __name__ == "__main__":
    config = {
        "user": 'eby',                 # Enter your own username
        "password": 'ebypw',             # Enter your own password
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
    ShowcaseApp().run()