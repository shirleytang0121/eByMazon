class SU():
    def __init__(self,cursor,suID):
        self.cursor = cursor
        self.ID = suID

    def manageApplication(self, applicationID, action):
        # action == True: approve: register GU to OU account and delete application, set password same as username
        # action == False: decline: delete it from application accounts

        self.cursor.execute("SELECT * FROM GUapplications WHERE applicationID = %s;" % applicationID)
        for info in self.cursor:
            username, email, name,card,address,state,  = info[2]


    def manageItem(self, itemID, action):
        # action == True: approve: change approvalStatus in ItemDB to True
        # action == False: decline: remove the item in ItemDB, add warning to post OU in warningDB
        pass

    def viewCompliant(self):
        # Get all compliant from DB, return array of dict{itemID, complianerID, description, compliantTime}
        pass

    def manageCompliant(self, itemID, complianerID, action):
        # action == True: remove: delete compliant in DB
        # action == False: justified: change the justified to True in DB
        #                  check for two justified compliant that will cause warning
        pass


    def itemBlacklist(self,itemID):
        # remove all the occurance of this item in DB
        # add to itBlacklist
        pass