import mysql.connector
from kivy.core.image import Image as CoreImage
from io import BytesIO
class General():
    def __init__(self,cursor):
        self.cursor = cursor

    def login_check(self, username, password):
        # check login info with DB
        # still need to implement for check OU status if is OU and GU application
        qry = "SELECT ID, userType FROM User WHERE username=%s AND password=%s;"
        self.cursor.execute(qry,(username,password))
        ID, userType = -1, -1
        for user in self.cursor:
            ID = user[0]
            userType = user[1]

        if ID == -1:
            return False
        return {'ID':ID, 'userType':userType}

    def getItemInfo(self, itemID):
        try:
            qry = "SELECT * FROM ItemInfo WHERE itemID = %s;" % itemID
            self.cursor.execute(qry, (itemID))


        except mysql.connector.Error as err:
            print("Error in getting item info to database")
            print(err)

    def popularItem(self):
        self.cursor.execute("SELECT itemID, image, title, description, priceType, usedStatus "
                            "FROM ItemInfo WHERE saleStatus = True;")
        allItem = []
        for info in self.cursor:
            # print(type(info[1]))

            # data = BytesIO(info[1])
            used,priceType = "No","FixedPrice"
            if info[4]:
                priceType="Bidding"
            if info[5]:
                used = "Yes"

            information = 'Description: ' + info[3] + '\nPrice Type: '+priceType +'\nUsed Status:'+used
            allItem.append({"itemID":info[0],"image":CoreImage(BytesIO(info[1]), ext="png").texture,"title":info[2],
                            "priceType":info[4],"info":information})
        return allItem

    def checkStaus(self, ouID):
        # return status of the select OU
        pass

    def changeStaus(self, ouID):
        #update new status
        # get call when receive warning or low rating
        pass

    def manageWarnig(self,ouID):
        # called when add a warning
        # check number warning receive, if greater or equal to 2, suspend OU
        # else make sure that ou is not VIP
        pass

    def ouBlacklist(self,ouID):
        # remove the ou from all DB and all active sale item post by that ou,
        # but not the sold item by he/she, the seller will be None
        # add the username to ouBlacklist
        pass

    def itemBlacklist(self,itemID):
        # remove all the occurance of this item in DB
        # add to itBlacklist
        pass
