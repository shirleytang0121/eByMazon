import mysql.connector
from mysql.connector import errorcode, OperationalError

from kivy.app import App
# from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
# from kivy.properties import StringProperty
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

    # Login Page
    def clearLogin(self):
        self.ids['loginUsername'].text = ""
        self.ids['loginPassword'].text = ""

    def cancelLogin(self):
        self.clearLogin()
        self.ids['screenmanager'].current = "homepage"

    def checkLogin(self,username,password):
        print("Username: %s \nPassword: %s" % (username,password))
        userInfo = general.login_check(username,password)

        if isinstance(userInfo, dict): # Success Login
            self.login = True
            self.ids['loginCheck'].text = ""
            self.clearLogin()  # clear login info for potential next user

            if userInfo['userType']:   # Create SU
                global su
                su = SU(cursor=cursor,suID=userInfo['ID'])
                self.ids['screenmanager'].current = "suHomepage"
            else:
                if userInfo['status'] == 2:
                    self.login = False
                    print("Suspend OU")
                    self.ids['loginCheck'].text = "You have receive 2 warning!!!\nYou are suspend by our system"
                # need a pop up page for appeal message
                elif userInfo['status'] == 3:
                    self.login = False
                    general.removeOU(ouID=userInfo['ID'],username=username)
                    self.ids['loginCheck'].text = "You have be removed by SU!!!\nYour information is now be delete"
                    print("Remove OU")
                # need to function to delete the OU in DB
                else:                   # Create OU
                    global ou
                    ou = OU(cursor=cursor,ouID = userInfo['ID'])
                    self.ids['screenmanager'].current = "homepage"



        else:   # Problem With Login
            self.login = False
            if userInfo == 1:
                self.ids['loginCheck'].text = "Your password is incorrect!!!"
            elif userInfo == 2:
                self.ids['loginCheck'].text = "Your application is still pending."
            elif userInfo == 3:
                self.ids['loginCheck'].text = "You are in the Blacklist!!!"
            else:
                self.ids['loginCheck'].text ="No User Found"

    # Sign up Page
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


    # Go to OU Account
    def toProfile(self):
        status = "VIP" if ou.status else "Ordinary User"
        self.ids['ouName'].text = "Name: %s" % ou.name
        self.ids['ouPhone'].text = "Phone: %s" % ou.phone
        self.ids['ouEmail'].text = "Email: %s"% ou.email
        self.ids['ouCard'].text = "Card Number: %s"% ou.card
        self.ids['ouAddress'].text = "Address: %s"% ou.address
        self.ids['ouState'].text = "State: %s"% ou.state
        self.ids['ouRate'].text = "Current Rating: %s"% ou.avgRate
        self.ids['ouMoney'].text = "Current Money Spend: %s"% ou.moneySpend
        self.ids['ouStatus'].text = "Current Status: %s"% status
        self.ids['ouStatusTime'].text = "Status Start Time: {:%b %d, %Y}".format(ou.statusTime)
        self.ids['screenmanager'].current = "profilePage"

    def editInfo(self):
        self.ids['editName'].text =  ou.name
        self.ids['editPhone'].text = ou.phone
        self.ids['editEmail'].text = ou.email
        self.ids['editCard'].text = ou.card
        self.ids['editAddress'].text = ou.address
        self.ids['editState'].text = ou.state
        self.ids['screenmanager'].current = "editPage"

    def changePassword(self):
        print("Change Password")
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

    def toItem(self):
        self.ids['screenmanager'].current = "itemPage"



    def friendLst(self):
        self.ids['screenmanager'].current = "friendPage"
    def history(self):
        self.ids['screenmanager'].current = "historyPage"




    def searchKeyword(self, word):
        self.displayItem()
        print(word)




    def friendlist(self):
        print('friendlist')

    # def history(self):
    #     print('history')

class eByMazonApp(App):
    # m = Manager()
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

    general = General(cnx=cnx,cursor=cursor)
    guest = GU(cnx=cnx,cursor=cursor)
    ou = None
    su = None
    eByMazonApp().run()