class GU():
    def __init__(self,cursor):
        self.cursor = cursor

    def checkUsername(self,username):
        # check if username not exist in DB and not in blacklist return False else return True
        pass

    def apply(self, username, email, name, card, address, state, phone):
        # check if username is already exist, not allow for duplicate username
        # If unique username, save the application to DB
        unique = self.checkUsername(username)
        if unique:
            return False

        qry = ("INSERT INTO GUapplications( username, email, name, cardNumber, address, state, phone) "
               "VALUE (%s,%s,%s,%s,%s);")
        self.cursor.execute(qry,(username, email, name, card, address, state, phone))


