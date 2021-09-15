import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta
from connect import cursor, cnx

#INITIALIZING DATABASE NAME
DB_NAME = 'supermarketdb'

#CREATE TABLE QUERIES
TABLES = {'product': (
    """ 
    CREATE TABLE product(
        ID INTEGER,
        Name VARCHAR(100),
        Quantity INTEGER,
        PRIMARY KEY(ID)
    )
    """
), 'food_drink': (
    """
    CREATE TABLE food_drink(
        ID INTEGER,
        Name VARCHAR(100),
        Quantity INTEGER,
        Foreign Key(ID) references product(ID)
    )
    """
), 'houseware': (
    """
    CREATE TABLE houseware(
        ID INTEGER,
        Name VARCHAR(100),
        Quantity INTEGER,
        Foreign Key(ID) references product(ID)
    )
    """
), 'other': (
    """
    CREATE TABLE other(
        ID INTEGER,
        Name VARCHAR(100),
        Quantity INTEGER,
        Foreign Key(ID) references product(ID)
    )
    """
), 'cleaning': (
    """
    CREATE TABLE cleaning(
        ID INTEGER,
        Name VARCHAR(100),
        Quantity INTEGER,
        Foreign Key(ID) references product(ID)
    )
    """
), 'In_log': (
    """
    CREATE TABLE in_log(
        ID INTEGER,
        Name VARCHAR(100),
        In_Quantity INTEGER,
        In_Date Date,
        EUD Date,
        In_Log_ID INTEGER,
        Price FLOAT,
        Foreign Key(ID) references product(ID),
        PRIMARY KEY(In_Log_ID)
    )
    """
), 'Out_log': (
    """
    CREATE TABLE Out_log(
        ID INTEGER,
        Name VARCHAR(100),
        Out_Quantity INTEGER,
        Out_Date Date,
        Out_Log_ID INTEGER,
        Foreign Key(ID) references product(ID),
        PRIMARY KEY(Out_Log_ID)
    )
    """

),
'User' : (
    """
    CREATE TABLE Registered_User(
        Username VARBINARY(100),
        Password VARBINARY(100),
        PRIMARY KEY(Username)
    )
    """
)}


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

#EXECUTING 'CREATE TABLE' QUERIES WITH FOR LOOP
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

# INSERTING QUERIES:
insert_product = """
        INSERT INTO product (ID, Name, Quantity) VALUES (123432, 'Toilet Paper', 10000);
        INSERT INTO product (ID, Name, Quantity) VALUES (756443, 'Sponges', 10000);
        INSERT INTO product (ID, Name, Quantity) VALUES (234234, 'Microfibre cloths', 1000);
        INSERT INTO product (ID, Name, Quantity) VALUES (645335, 'Brush', 1000);
        INSERT INTO product (ID, Name, Quantity) VALUES (876534, 'Bucket', 1000);
        INSERT INTO product (ID, Name, Quantity) VALUES (865235, 'Protective Gloves', 5000);
        INSERT INTO product (ID, Name, Quantity) VALUES (325326, 'Meat', 5000);
        INSERT INTO product (ID, Name, Quantity) VALUES (965343, 'Fish', 1000);
        INSERT INTO product (ID, Name, Quantity) VALUES (542455, 'Cake', 2000);
        INSERT INTO product (ID, Name, Quantity) VALUES (523445, 'Ice Tea', 2000);
        INSERT INTO product (ID, Name, Quantity) VALUES (745652, 'Coke', 2000);
        INSERT INTO product (ID, Name, Quantity) VALUES (435346, 'Pillow', 3000);
        INSERT INTO product (ID, Name, Quantity) VALUES (532676, 'Blanket', 3000);
        INSERT INTO product (ID, Name, Quantity) VALUES (121346, 'Earphone', 3000);
        INSERT INTO product (ID, Name, Quantity) VALUES (643342, 'Phone Charger', 5000);
        INSERT INTO product (ID, Name, Quantity) VALUES (845634, 'Battery', 5000);
        """

insert_cleaning = """
        INSERT INTO cleaning (ID, Name, Quantity) VALUES (123432, 'Toilet Paper', 10000);
        INSERT INTO cleaning (ID, Name, Quantity) VALUES (756443, 'Sponges', 10000);
        INSERT INTO cleaning (ID, Name, Quantity) VALUES (234234, 'Microfibre cloths', 1000);
        INSERT INTO cleaning (ID, Name, Quantity) VALUES (645335, 'Brush', 1000);
        INSERT INTO cleaning (ID, Name, Quantity) VALUES (876534, 'Bucket', 1000);
        INSERT INTO cleaning (ID, Name, Quantity) VALUES (865235, 'Protective Gloves', 5000);
        """

insert_food_drink = """
        INSERT INTO food_drink (ID, Name, Quantity) VALUES (325326, 'Meat', 5000);
        INSERT INTO food_drink (ID, Name, Quantity) VALUES (965343, 'Fish', 1000);
        INSERT INTO food_drink (ID, Name, Quantity) VALUES (542455, 'Cake', 2000);
        INSERT INTO food_drink (ID, Name, Quantity) VALUES (523445, 'Ice Tea', 2000);
        INSERT INTO food_drink (ID, Name, Quantity) VALUES (745652, 'Coke', 2000);
        """

insert_houseware = """
        INSERT INTO houseware (ID, Name, Quantity) VALUES (435346, 'Pillow', 3000);
        INSERT INTO houseware (ID, Name, Quantity) VALUES (532676, 'Blanket', 3000);
        """

insert_other = """
        INSERT INTO other (ID, Name, Quantity) VALUES (121346, 'Earphone', 3000);
        INSERT INTO other (ID, Name, Quantity) VALUES (643342, 'Phone Charger', 5000);
        INSERT INTO other (ID, Name, Quantity) VALUES (845634, 'Battery', 5000);
        """

insert_in_log = """
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (756443,  'Sponges',              '2021-4-28',    NULL,           986214281, 9000, 1100);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (756443,  'Sponges',              '2021-4-28',    NULL,           564214282, 1100, 1200);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (234234,  'Microfibre cloths',    '2021-4-28',    NULL,           234214283, 1000, 1300);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (645335,  'Brush',                '2021-3-20',    NULL,           432213201, 1000, 4000);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (876534,  'Bucket',               '2021-2-20',    NULL,           643213202, 1000, 5000);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (865235,  'Protective Gloves',    '2021-2-20',    NULL,           523213203, 5000, 10000);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (325326,  'Meat',                 '2021-2-20',    '2021-5-20',    312212201, 5000, 200);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (965343,  'Fish',                 '2021-2-20',    '2021-3-20',    123212202, 1000, 1000);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (542455,  'Cake',                 '2021-2-20',    '2021-3-1',     325212203, 2000, 10000);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (523445, 'Ice Tea',              '2021-2-20',     '2021-10-20',   546212204, 2000, 2000);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (745652, 'Coke',                 '2021-2-20',     '2022-1-1',     865212205, 2000, 9000);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (435346, 'Pillow',               '2021-2-20',     NULL,           452212206, 3000, 2000);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (532676, 'Blanket',              '2021-1-10',     NULL,           235211101, 3000, 2000);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (121346, 'Earphone',             '2021-1-10',     NULL,           235211102, 3000, 2200);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (643342, 'Phone Charger',        '2021-1-10',     NULL,           562211103, 5000, 1000);
        INSERT INTO In_log (ID, Name, In_Date,   EUD, In_Log_ID, In_Quantity,  Price) VALUES (845634, 'Battery',              '2021-1-10',     NULL,           256211104, 5000, 1000);
        """

insert_out_log = """
        INSERT INTO Out_log (ID, Name, Out_Quantity, Out_Date, Out_Log_ID) VALUES (756443, 'Sponges', 100, '2021-4-29', 525214291);
        """

insert_user = """
    INSERT INTO Registered_User (Username, Password) VALUES ('Yigit', '123');
    INSERT INTO Registered_User (Username, Password) VALUES ('Hamza', '123');
    INSERT INTO Registered_User (Username, Password) VALUES ('ABC','123');
"""

# INSERT FUNCTION
def insert(query):
    for result in cursor.execute(query, multi=True):
        if result.with_rows:
            print("Rows produced by statement '{}':".format(
            result.statement))
            print(result.fetchall())
        else:
            print("Number of rows affected by statement '{}': {}".format(
            result.statement, result.rowcount))

# QUERIES EXECUTED USING INSERT FUNCTION (COMMENT OUT)
insert(insert_product)
insert(insert_cleaning)
insert(insert_other)
insert(insert_houseware)
insert(insert_food_drink)
insert(insert_in_log)
insert(insert_out_log)
insert(insert_user)

cnx.commit()


# CLOSING CURSOR AND CONNECTION
cursor.close()
cnx.close()

