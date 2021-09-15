import mysql.connector
from mysql.connector import errorcode
DB_NAME = 'supermarketdb'
#CREATING CONNECTION
try:
    cnx = mysql.connector.connect(  user='root',
                                    password='3553H',
                                    host='127.0.0.1')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

#CREATING CURSOR
cursor = cnx.cursor()

#CREATING DATABASE
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("FAILED TO CREATE DATABASE, ERROR -> {}".format(err))
        exit(1)

#USING DATABASE IN ORDER TO CREATE TABLES
try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
        cursor.execute("USE {}".format(DB_NAME))
    else:
        print(err)
        exit(1)