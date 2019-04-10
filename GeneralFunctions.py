class General():
    def __init__(self,cursor):
        self.cursor = cursor

    def login_check(self, username, password):

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




