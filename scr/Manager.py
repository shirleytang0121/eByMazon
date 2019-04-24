# mysql
import mysql.connector
import os
import datetime
from mysql.connector import errorcode
# kivy
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.floatlayout import FloatLayout

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


################### Home Page Item Recycle View ################################
class item(BoxLayout):
    # the item frame in homepage, implemented in feature.kv
    def getItem(self):

        if self.priceType:
            root.tobidItem(self.itemIndex)
        else:
            root.tofixedItem(self.itemIndex)


################################### Sign Up Page ################################
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


########################## Appeal Pop Up Page ################################
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


########################## OU Item Page ################################
class LoadImage(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class ouItem(Screen):
    '''global variables:
    isDate(true), isTitle(true),
    isDescription(true), isNumber(True), isImage(True), isPrice(True)
    isNew(False), isUsed(False)
    '''


    def backProfile(self):
        root.toProfile()

    def backPostItemPage(self):
        root.getOUitem()
        self.ids["ouItemManager"].current = "itemHome"
        self.clearBidItemInput()
        self.clearFixedItemInput()

    ################### Clear FUNCTIONS ################
    def clearBidItemInput(self):
        self.ids['itemTitle'].text = ""
        self.ids['itemDescription'].text = ""
        self.ids['itemPrice'].text = ""
        self.ids['itemBidDay'].text = ""
        self.ids['image'].text = "Choose Image"
        self.ids['bidItemWarning'].text = ""
        self.ids['new'].active = False
        self.ids['used'].active = False
        self.image = ""

    def clearFixedItemInput(self):
        self.ids['itemTitle1'].text = ""
        self.ids['itemDescription1'].text = ""
        self.ids['itemPrice1'].text = ""
        self.ids['itemNumbers1'].text = ""
        self.ids['fixedItemWarning'].text = ""
        self.image = ""
        # self.isTitle, self.isDescription, self.isPrice, self.isNumber = True, True, True, True

    ############ Getting image #########
    def getImage(self):
        content = LoadImage(load=self.loadImage, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    def loadImage(self,path, filename):
        with open(os.path.join(path, filename[0]),'rb') as file:
            self.image = file.read()
        filename= str(filename[0])
        filename = filename.split('/')
        self.ids['image'].text = filename[-1]
        self.ids['image1'].text = filename[-1]
        self._popup.dismiss()
    def dismiss_popup(self):
        self._popup.dismiss()

    ################### Check FUNCTIONS ################
    def checkEmpty(self, input):
        if input is None or input == '':
            return False
        return True

    def checkInt(self, input):
        if input is None or input == '':
            return False
        try:
            int(input)
            return True
        except ValueError:
            return False

    def checkFloat(self, input):
        if input is None or input == '':
            return False
        return isinstance(input, float) or self.checkInt(input)

    def updateStatus(self, status):
        self.isUsed = status

    ################### Submit FUNCTIONS ################
    def submitBidingItem(self, title, description, itemPrice, itemBidDay):
        if not(self.checkEmpty(title) or self.checkEmpty(description) or self.checkFloat(itemPrice) or self.checkInt(itemBidDay)):
            condition = False
        else:
            try:
                used = self.isUsed
                image = self.image
                condition = True
                if image == "":
                    condition = False
            except AttributeError as err:
                print(err)
                condition = False

        if not condition or not (self.ids['new'].active or self.ids['used'].active):
            self.ids['bidItemWarning'].text = "Fail to Submit!!! Input should not be empty\
            \nStart Price should be an number (integer or decimal), one checkbox should be checked.\
            \nBid Day should be integer, for how many days you want bidding last."

        else:
            self.ids['bidItemWarning'].text = ""
            ou.submitBiddingItem(image=self.image,title=title,description=description,
                                 usedStatus=self.isUsed,startPrice=float(itemPrice),endDay=int(itemBidDay))
            print("submitted")
            self.clearBidItemInput()
            self.backPostItemPage()

    def submitFixedItem(self, title, description, itemPrice, number_available):
        if not(self.checkEmpty(title) or self.checkEmpty(description) or self.checkFloat(itemPrice) or self.checkInt(number_available)):
            condition = False
        else:
            try:
                image = self.image
                condition = True
                if image == "":
                    condition = False
            except AttributeError as err:
                print(err)
                condition = False

        if not condition:
            self.ids['fixedItemWarning'].text = "Fail to Submit!!!\nInput should not be Empty!\
            \nPrice should be integer or decimal.\
            \nNumber available should be integer."
        else:
            self.ids['fixedItemWarning'].text = ""
            ou.submitFixedPriceItem(image=self.image, title=title, description=description,
                                    price=float(itemPrice), available=int(number_available))

            print("submitted")
            self.clearFixedItemInput()
            self.backPostItemPage()

    ######################### QUERY #############################
    # def postBidItem(self, title, description, itemPrice, itemBidDay):
    #     try:
    #         query()
    #         self.cursor.execute(query())
    #         self.cnx.commit()
    #         return True
    #     except mysql.connector.Error as ERR:
    #         print("Error in Applying OU Account: %s" % ERR)
    #         return False
    #
    # def postFixedItem(self, title, description, itemPrice, number_available):
    #     try:
    #         query()
    #         self.cursor.execute(query())
    #         self.cnx.commit()
    #         return True
    #     except mysql.connector.Error as ERR:
    #         print("Error in Applying OU Account: %s" % ERR)
    #         return False


################################### Other Pages ################################
class GUapplication(Screen):
    def tohome(self):
        root.ids['screenmanager'].current = "suHomepage"
class ouInfo(Screen):
    def tohome(self):
        root.ids['screenmanager'].current = "suHomepage"
class itemManage(Screen):
    def tohome(self):
        root.ids['screenmanager'].current = "suHomepage"
class itemFixed(Screen):
    status = BooleanProperty()


####################### TO BE FILLED #################
class editPassword(FloatLayout):
    back = ObjectProperty(None)
    submit = ObjectProperty(None)

def convert_data(data):
    l = []
    for item in data:
        for key, value in item.items():
            l.append({'text': key, 'value': str(value)})
    return l

class friendList(Screen):
    def backProfile(self):
        root.toProfile()

    def displayFriend(self):
        #fetching from database
        arr = ({'Item1': 5000},{'Item2': 1000})
        # convert to [{'text': 'Item1', 'value': 5000}, {'text': 'Item2', 'value': 1000}]
        self.ids['rv'].data = convert_data(arr)

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


####################### Main Class #############################

class Manager(Screen):
    login = BooleanProperty()
    ouID = ObjectProperty()
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.displayItem()


    ####################### Display Homepage Item #############################

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


    ####################### Homepage Two Button #############################

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


    ####################### Login Page Function #############################

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
                    ou = OU(cnx=cnx, cursor=cursor,ouID = self.ouID)
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


    ####################### Goto OU Profile #############################

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


    ###################### Change Password and Ou Info ###################
    def getPassword(self):
        content = editPassword(back=self.dismiss_popup, submit=self.changePassword)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    def dismiss_popup(self):
        self._popup.dismiss()

    def changePassword(self,newpassword):
        print("Change Password %s" % newpassword)
        ou.changePassword(newpassword)
        self.dismiss_popup()

    def changeInfo(self,name, card, email, phone, address, state):
        # Check....... inputs, add warning label
        ou.updateOUInfo(name, card, email, phone, address, state)
        self.toProfile()


    ###################### Other ###################
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

    def getOUitem(self):
        ouItems = ou.getItem()
        waitI = []
        fixedI = []
        bidI = []

        for item in ouItems:
            typeStr = "Bidding" if item.priceType else "Fixed Price"
            if not item.approvalStatus:
                waitI.append({"image": item.image,"title": item.title, "priceType": item.priceType,
                              "price": str(item.price), "typeStr": typeStr, "description": item.descrpition})
            else:
                # sale = "Sold" if item.saleStatus else "On Sale"
                try:
                    highestPrice = str(item.highestPrice)
                except AttributeError:
                    highestPrice = "None"

                saleStatus = False
                if item.saleStatus:
                    saleStatus = True
                if item.priceType:
                    bidI.append({"image": item.image, "title": item.title,"price": str(item.price),
                                 "currentBid": highestPrice, "typeStr": typeStr,
                                 "description": item.descrpition, "reviews": str(item.views),
                                 "likes": str(item.likeness), "dislike": str(item.dislike), "status": saleStatus})

                else:
                    fixedI.append({"image": item.image, "title": item.title,"price": str(item.price),
                                 "numLeft": str(item.available), "typeStr": typeStr,
                                 "description": item.descrpition, "reviews": str(item.views),
                                 "likes": str(item.likeness), "dislike": str(item.dislike), "status": saleStatus})

        self.ids["ouItem"].ids["waitItem"].data = waitI
        self.ids["ouItem"].ids["itemFixed"].data = fixedI
        self.ids["ouItem"].ids["itemBid"].data = bidI

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
        self.getOUitem()
        self.ids['screenmanager'].current = "ouItem"
class eByMazonApp(App):

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