import mysql.connector
class GU():
    def __init__(self,cursor):
        self.cursor = cursor

    def checkUsername(self,username):
        # check if username not exist in DB and not in blacklist return False else return True
        self.cursor.execute("SELECT * from User;")
        k1 = self.cursor.fetchone()
        qry = "SELECT EXISTS(SELECT * from User WHERE username='%s');" % username
        self.cursor.execute(qry)

        k = self.cursor.fetchone()[0]
        if k:
            return False
        return True
        # pass

    def apply(self, username, name, email, card, address, state, phone):
        # check if username is already exist, not allow for duplicate username
        # If unique username, save the application to DB
        unique = self.checkUsername(username)
        if not unique:
            return False
        try:
            qry = ("INSERT INTO GUapplications( username, email, name, cardNumber, address, state, phone) "
                   "VALUE (%s,%s,%s,%s,%s,%s,%s);")
            self.cursor.execute(qry,(username, email, name, card, address, state, phone))
            return True
        except mysql.connector.Error as ERR:
            print(ERR)
            return False


