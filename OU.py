from mysql.connector import OperationalError
class OU():
    def __init__(self,cursor,ouID):
        self.cursor = cursor
        self.ID = ouID
        profile = self.getOUInfo()
        self.name, self.card, self.address, self.state, self.phone = self.getOUInfo(ouID)

    def getOUInfo(self):
        # Return ou information in strings: name, card number, address, state, phone
        self.cursor.execute("SELECT * FROM OU WHERE ouID = %s"% self.ID)
        for info in self.cursor:
            return [info[1],info[2],info[3],info[4],info[5]]

    def updateOUInfo(self, name, card, phone, address, state):
        # update OU in DB
        qry = "UPDATE OU SET name = %s, cardNumber= %s, address =%s, state =%s, phone=%s WHERE ouID=%s;"

        try:
            self.cursor.execute(qry,(name, card,address,state,phone,self.ID))
            return True
        except OperationalError:
            print("Error in update OU Info")
            return False

    def changePassword(self,password):
        #update password in DB
        print()
    def transactionHistory(self,itemID):
        # get transaction History
        print()
