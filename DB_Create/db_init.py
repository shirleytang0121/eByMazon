# If you don't have mysql.connect library
# Run `pip install mysql-connector` to install

import mysql.connector
from mysql.connector import errorcode, OperationalError

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

def insertItemInfo(cursor, itemID, image, title, priceType,saleStatus):
    try:
        image1 = convertToBinaryData(image)
        qry = ("INSERT INTO ItemInfo(itemID, image, title, priceType, saleStatus) VALUE (%s,%s,%s,%s,%s)"
               "ON DUPLICATE KEY UPDATE image=%s, title=%s, priceType=%s, saleStatus=%s;")
        result = cursor.execute(qry, (itemID,image1,title,priceType,saleStatus,image1,title,priceType,saleStatus))
        cnx.commit()
    except mysql.connector.Error as err:
        print("Error in insert item info to database")
        print(err)

def getItemInfo(cursor, itemID):
    try:
        qry = "SELECT image FROM ItemInfo WHERE itemID = %s;"%itemID
        cursor.execute(qry, (itemID))
        for image in cursor:
            write_file(image[0],'test.jpg')
    except mysql.connector.Error as err:
        print("Error in getting item info to database")
        print(err)


def executeScriptsFromFile(cnx, cursor,filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')


    for command in sqlCommands:
        try:
            cursor.execute(command)
            cnx.commit()
        except OperationalError:
            print("Command skipped: ")
if __name__  == "__main__":
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



    # Create relations in DB
    print("Create eByMazon")
    executeScriptsFromFile(cnx, cursor, 'schema.sql')
    # If take to long to run this command, means you didn't fully close all the connection of this database,
    # Run below code in terminal:
        #   mysqladmin processlist -u username -p            -- replace your own username with the username
        #   mysqladmin kill id -u username -p                -- replace the id with the process id of your database



    # Insert values to other tables
    print("Insert Values to eByMazon")
    executeScriptsFromFile(cnx,cursor,'insertValues.sql')

    # Insert State Sale Tax Rates
    print("Insert State Sale Tax Rates")
    executeScriptsFromFile(cnx,cursor,'Insert_Taxes_Rate.sql')

    # Insert Item info
    # Maximum size currently an image can have is 64KB
    print("Insert Item Info")
    insertItemInfo(cursor, 1,"images/item1.jpg","SHE Forever CD",False, True)
    insertItemInfo(cursor,2,"images/item2.jpg","SHE Shero DVD",False, True)
    insertItemInfo(cursor,3,"images/item3.jpg","Harry Potter Book Series",False, True)
    insertItemInfo(cursor,4,"images/item4.jpg","The Hunger Games by suzanne collins",False, True)
    insertItemInfo(cursor,5,"images/item5.jpg","Samsung 17-Inch Series 7 Chronos Laptop",False, True)
    insertItemInfo(cursor,6,"images/item6.jpg","Macbook Air 13-Inch, pink",False, True)
    cnx.commit()        #Need to make sure everything push to database

# Test get image
# getItemInfo(cursor, 1)
# print()
