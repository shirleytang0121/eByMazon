import mysql.connector
class General():
    def __init__(self,cursor):
        self.cursor = cursor

    def login_check(self, username, password):
        # check login info with DB
        # still need to implement for check OU status if is OU and GU application
        self.cursor.execute(
            "SELECT ID, userType FROM User WHERE username=%s, password=%s",
            (username,password))

        ID, userType = -1, -1
        for user in self.cursor:
            ID = user[0]
            userType = user[1]

        if ID == -1:
            return False
        return {'ID':ID, 'userType':userType}




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
