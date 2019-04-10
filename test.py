# Test DB functions
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

from ou import OU

config = {
    "user": '',
    "password": '',
    "host": '127.0.0.1',
    "database": 'eByMazon'
}

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    ou = OU(cursor,2)

except mysql.connector.Error as error:
    print("Error in connecting database %s" % config["database"])
    print("The error is %s", error)


print(ou.name)
print(ou.card)
