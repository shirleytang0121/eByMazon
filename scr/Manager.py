# mysql
import mysql.connector
import numbers
import datetime
from mysql.connector import errorcode
# kivy
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen #ScreenManager, FadeTransition
from kivy.properties import BooleanProperty,NumericProperty
from kivy.lang import Builder
from kivy.core.window import Window

# self define classes
try:
    from scr.GeneralFunctions import General
    from scr.GU import GU
    from scr.SU import SU
    from scr.OU import OU
    from scr.Item import Item
    from scr.otherClass import *
except ModuleNotFoundError:
    from GeneralFunctions import General
    from GU import GU
    from SU import SU
    from OU import OU
    from Item import Item
    from otherClass import *

class item(BoxLayout):
    # the item frame in homepage, implemented in feature.kv
    def getItem(self):

        if self.priceType:
            root.tobidItem(self.itemIndex)
        else:
            root.tofixedItem(self.itemIndex)

class Signup(Screen):
    # sign up page implement in signup.kv
    stateV,cardV,nameV = BooleanProperty(),BooleanProperty(),BooleanProperty()

    def tohome(self):
        root.tohome()

    def clearSignup(self):
        self.ids['GUusername'].text = ""
        self.ids['GUname'].text = ""
        self.ids['GUphone'].text = ""
        self.ids['GUemail'].text = ""
        self.ids['GUaddress'].text = ""
        self.ids['GUState'].text = ""
        self.ids['GUcard'].text = ""

        self.ids['warnApplication'].text = ""
        self.ids['warnUsername'].text = ""
        self.stateV, self.cardV, self.nameV = True, True,True

    def checkUsername(self,username):
        nameCheck = guest.checkUsername(username)
        if not nameCheck:
            self.ids['warnUsername'].text = "Username can be used"
        elif nameCheck == 1:
            self.ids['warnUsername'].text = "Username already existed in system"
        elif nameCheck == 2:
            self.ids['warnUsername'].text = "Username already existed in system"
        elif nameCheck == 3:
            self.ids['warnUsername'].text = "Username are in system blacklist!"

    def checkName(self,name):
        self.nameV = not guest.checkInput(name)

    def checkState(self,state):
        self.stateV = guest.checkState(state.upper())

    def checkCard(self,card):
        self.cardV = not guest.checkInput(card)

    def signUp(self,username, name, phone, email,address,state,card):
        self.checkName(name)
        self.checkState(state)
        self.checkCard(card)
        self.checkUsername(username)
        if guest.checkUsername(username) or not self.stateV or not self.cardV or not self.nameV:
            self.ids['warnApplication'].text = "Fail to Apply!!!"
        else:
            applied = guest.apply(username, name, email,card,address,state.upper(),phone)
            self.ids['warnApplication'].text = "Fail to Apply!!!" # for not approve application
            if applied:                                      # save on DB
                self.ids['warnApplication'].text = ""
                self.clearSignup()
                root.tohome()

class GUapplication(Screen):
    def tohome(self):
        root.ids['screenmanager'].current = "suHomepage"
class ouInfo(Screen):
    def tohome(self):
        root.ids['screenmanager'].current = "suHomepage"
class itemManage(Screen):
    def tohome(self):
        root.ids['screenmanager'].current = "suHomepage"

class appealPop(Popup):
    def homepage(self):
        appealPop.dismiss(self)
        root.clearLogin()
        root.tohome()

    def switchScreen(self, screenName):
        self.ids['appealManager'].current = screenName

    def removeOU(self):
        general.removeOU(username=root.ids['loginUsername'].text)
        self.homepage()

    def appeal(self,message):
        general.appeal(ouID=root.ouID,message=message)
        self.homepage()


class ouItem(Screen):
    '''global variables: 
    isDate(true), isTitle(true),
    isDescription(true), isNumber(True), isImage(True), isPrice(True)
    isNew(False), isUsed(False)
    '''
    def backProfile(self):
        root.toProfile()
    def backPostItemPage(self):
        self.ids["ouItemManager"].current = "itemHome"
        self.clearBidItemInput()
        self.clearFixedItemInput()
 
    def checkTitle(self,input):
        self.isTitle = not self.checkEmpty(input)
    def checkDescription(self,input):
        self.isDescription = not self.checkEmpty(input)
    def checkDate(self,input):
        self.isDate = self.checkDateTime(input)
        # self.isDate = not self.checkEmpty(input)
    def checkNumber(self,input):
        self.isNumber = self.checkInt(input)
    def checkImage(self,input):
        self.isImage = not self.checkEmpty(input)
    def checkPrice(self,input):
        self.isPrice = self.checkFloat(input)
    def updateStatus(self, input):
        if input=='used':
            self.isNew = False
            # self.isUsed = True
        elif input == 'new':
            # self.isNew = True
            self.isUsed = False
        
    def submitBidingItem(self,title,description, itemPrice, itemBidDay):
        self.checkTitle(title)
        self.checkDescription(description)
        self.checkPrice(itemPrice)
        self.checkDate(itemBidDay)
        # self.checkImage(image)

        result = self.isTitle and self.isDescription and self.isDate and self.isPrice and (self.isNew != self.isUsed)

        if not result:
            self.ids['bidItemWarning'].text = "Fail to Submit!!! Input should not be empty\
            \nStart Price should be integer or decimal, one checkbox should be checked\
            \nBid Day should follow format of YYYY-MM-DD"
            self.clearBidItemInput()
        else:
            self.ids['bidItemWarning'].text = ""
            print("submitted")
            self.clearBidItemInput()
            root.toProfile()

    def submitFixedItem(self,title, description, itemPrice, number_available):
        self.checkTitle(title)
        self.checkDescription(description)
        self.checkPrice(itemPrice)
        self.checkNumber(number_available)
        # self.checkImage(image)

        result = self.isTitle and self.isDescription and self.isNumber and self.isPrice
        if not result:
            self.ids['fixedItemWarning'].text = "Fail to Submit!!!\nInput should not be Empty\
            \nPrice should be integer or decimal\
            \nNumber available should be integer"
        else:
            self.ids['fixedItemWarning'].text = ""
            print("submitted")
            self.clearFixedItemInput()
            root.toProfile()
################### HELPER FUNCTIONS ################
    def checkEmpty(self,input):
        if input is None or input=='':
            return True
        return False
    def checkInt(self, input):
        try:
            int(input)
            return True
        except ValueError:
            return False
    def checkFloat(self,input):
        return isinstance(input, float) or self.checkInt(input)
    def checkDateTime(self,input):
        try:
            datetime.datetime.strptime(input, '%Y-%m-%d')
            return True
        except ValueError:
            print('date not accepted')
            return False
    def clearBidItemInput(self):
        self.ids['itemTitle'].text = ""
        self.ids['itemDescription'].text = ""
        self.ids['itemPrice'].text = ""
        self.ids['itemBidDay'].text = ""
        self.ids['new'].active = False
        self.ids['used'].active = False

        self.isTitle, self.isDescription, self.isPrice,self.isDate,self.isNew, self.isUsed = True,True,True,True,True,True
    def clearFixedItemInput(self):
        self.ids['itemTitle1'].text = ""
        self.ids['itemDescription1'].text = ""
        self.ids['itemPrice1'].text = ""
        self.ids['itemNumbers1'].text = ""
        self.isTitle, self.isDescription, self.isPrice, self.isNumber = True,True,True,True

######################### QUERY #############################
    def postBidItem(self,title, description, itemPrice, itemBidDay):
        try:
            query()
            self.cursor.execute(query())
            self.cnx.commit()
            return True
        except mysql.connector.Error as ERR:
            print("Error in Applying OU Account: %s" % ERR)
            return False
    def postFixedItem(self,title, description, itemPrice, number_available):
        try:
            query()
            self.cursor.execute(query())
            self.cnx.commit()
            return True
        except mysql.connector.Error as ERR:
            print("Error in Applying OU Account: %s" % ERR)
            return False

####################### TO BE FILLED #################
class friendList(Screen):
    def backProfile(self):
        root.toProfile()
class transactionHistory(Screen):
    def backProfile(self):
        root.toProfile()
class fixedItem(Screen):
    itemIndex = NumericProperty()
    user = BooleanProperty()
    def tohome(self):
        root.tohome()
    def dislikeItem(self,name):
        root.dislikeItem(name,self.itemIndex)
    def likeItem(self,name):
        root.likeItem(name,self.itemIndex)

class biddingItem(Screen):
    itemIndex = NumericProperty()
    user = BooleanProperty()
    def tohome(self):
        root.tohome()
    def dislikeItem(self,name):
        root.dislikeItem(name,self.itemIndex)
    def likeItem(self,name):
        root.likeItem(name,self.itemIndex)

class Manager(Screen):
    login = BooleanProperty()
    ouID = ObjectProperty()
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.displayItem()

    # ###### Display Item
    def displayItem(self):
        global items
        items = general.popularItem()
        returndict = []
        i = 0
        for item in items:
            typeStr = "Bidding" if item.priceType else "Fixed Price"
            returndict.append({"itemIndex": i,"image": item.image,"title":item.title, "priceType":item.priceType,
                               "price":str(item.price),"reviews": str(item.views), "likes": str(item.likeness),
                               "typeStr": typeStr})
            i+= 1
        self.ids['rv'].data = returndict


    def tologin(self):
        if self.login:
            self.login = False
        else:
            self.ids['screenmanager'].current = "loginpage"
    def signProfile(self):
        if self.login:
            self.toProfile()
        else:
            self.signup()

    # Login Page
    def clearLogin(self):
        self.ids['loginUsername'].text = ""
        self.ids['loginPassword'].text = ""

    def cancelLogin(self):
        self.clearLogin()
        self.ids['screenmanager'].current = "homepage"
    def suLogout(self):
        self.login = False
        self.ids['screenmanager'].current = "homepage"

    def checkLogin(self,username,password):
        print("Username: %s \nPassword: %s" % (username,password))
        userInfo = general.login_check(username,password)

        if isinstance(userInfo, dict): # Success Login
            self.login = True
            self.ids['loginCheck'].text = ""
            if userInfo['userType']:   # Create SU
                global su
                su = SU(cursor=cursor,suID=userInfo['ID'])
                self.ids['screenmanager'].current = "suHomepage"
                self.clearLogin()  # clear login info for potential next user
            else:
                self.ouID = userInfo['ID']
                if userInfo['status'] >= 2: # suspend or in blacklist
                    self.login = False
                    appeal = appealPop()
                    if userInfo['status'] == 3: # in blacklist
                        appeal.ids["appealManager"].current = 'removed'
                    appeal.open()
                else:                   # Create OU
                    global ou
                    ou = OU(cursor=cursor,ouID = self.ouID)
                    self.ids['screenmanager'].current = "homepage"
                    self.clearLogin()  # clear login info for potential next user

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



    def tohome(self):
        self.displayItem()
        self.ids['screenmanager'].current = "homepage"


    def signup(self):
        self.ids['screenmanager'].current = "signupPage"


    def tofixedItem(self,itemIndex):
        item = items[itemIndex]
        item.addView()

        self.ids['fixedItem'].itemIndex = itemIndex
        self.ids['fixedItem'].user = not self.login
        self.ids['fixedItem'].ids['itemImage'].texture = item.image
        self.ids['fixedItem'].ids['itemTitle'].text = item.title
        self.ids['fixedItem'].ids['itemDescription'].text=item.descrpition
        self.ids['fixedItem'].ids['itemPrice'].text="$"+str(item.price)
        self.ids['fixedItem'].ids['itemAvailable'].text = str(item.available)
        self.ids['fixedItem'].ids['itemLike'].text = str(item.likeness)
        self.ids['fixedItem'].ids['itemDislike'].text = str(item.dislike)
        self.ids['screenmanager'].current = "fixedItem"

    def tobidItem(self,itemIndex):
    #     global item
    #     item = Item(cursor=cursor,itemID=itemID)
        item = items[itemIndex]
        item.addView()
        self.ids['biddingItem'].user = not self.login
        self.ids['biddingItem'].itemIndex = itemIndex
        self.ids['biddingItem'].ids['itemImage'].texture = item.image
        self.ids['biddingItem'].ids['itemTitle'].text = item.title
        self.ids['biddingItem'].ids['itemDescription'].text=item.descrpition
        self.ids['biddingItem'].ids['itemPrice'].text="$"+str(item.price)
        self.ids['biddingItem'].ids['itemLike'].text = str(item.likeness)
        self.ids['biddingItem'].ids['itemDislike'].text = str(item.dislike)
        self.ids['biddingItem'].ids['itemUsed'].text = str(item.usedStatus)
        try:
            self.ids['biddingItem'].ids['itemBid'].text = "$" + str(item.highestPrice)
        except AttributeError:
            self.ids['biddingItem'].ids['itemBid'].text = "None"
        self.ids['screenmanager'].current = "biddingItem"

    # ###############
    def likeItem(self,pagename,itemIndex):
        items[itemIndex].likeItem(ou.ID)
        self.ids[pagename].ids['itemLike'].text = str(items[itemIndex].likeness)

    def dislikeItem(self,pagename,itemIndex):
        items[itemIndex].dislikeItem(ou.ID)
        self.ids[pagename].ids['itemDislike'].text = str(items[itemIndex].dislike)

    def friendList(self):
        print('friendlist')
        self.ids['screenmanager'].current = "friendPage"
    def history(self):
        print('history')
        self.ids['screenmanager'].current = "historyPage"

    def searchKeyword(self, word):
        self.displayItem()
        print(word)
    def toguApply(self):
        self.ids['screenmanager'].current = "GUapplication"
        print("In GU")
    def toouInfo(self):
        self.ids['screenmanager'].current = "ouInfo"
    def toitemManage(self):
        self.ids['screenmanager'].current = "itemManage"

    def toOuItem(self):
        self.ids['screenmanager'].current = "ouItem"
class eByMazonApp(App):
    # m = Manager()
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Builder.load_file("manage.kv")
        global root
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
        cnx.set_unicode(value=True)
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
    ou,su,items = None,None,None
    eByMazonApp().run()