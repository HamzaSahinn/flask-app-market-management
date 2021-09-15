from random import  randint
from connect import cursor
import operator

def generate_product_id():
    num = randint(100000, 999999)

    query = """
    SELECT ID FROM product;
    """
    cursor.execute(query)
    row = cursor.fetchall()

    isFound = True
    while(True):
        for r in row:
            if (r[0] == num):
                num = randint(100000, 999999)
                isFound = False
                break
        if isFound:
            return num
        isFound = True


def generate_in_log_id():
    num = randint(100000000, 999999999)
    query = """
    SELECT In_Log_ID FROM In_Log;
    """
    cursor.execute(query)
    row = cursor.fetchall()

    isFound = True
    while (True):
        for r in row:
            if (r[0] == num):
                num = randint(100000000, 999999999)
                isFound = False
                break
        if isFound:
            return num
        isFound = True

def generate_out_log_id():
    num = randint(100000000, 999999999)

    query = """
    SELECT Out_Log_ID FROM Out_Log;
    """
    cursor.execute(query)
    row = cursor.fetchall()

    isFound = True
    while (True):
        for r in row:
            if (r[0] == num):
                num = randint(100000000, 999999999)
                isFound = False
                break
        if isFound:
            return num
        isFound = True

def is_unqiue(name):
    name = name.lower()
    query_name = """
    SELECT product.name FROM product;
    """

    cursor.execute(query_name)
    row = cursor.fetchall()

    for r in row:
        if(r[0].lower() == name):
            query_id = """
            SELECT product.ID, product.Quantity FROM product WHERE product.Name='{}';
            """.format(name)

            cursor.execute(query_id)
            row = cursor.fetchall()
            return row[0]

    return (-1,-1)

def check_user(username, password):
    query = """
    SELECT * FROM Registered_User WHERE 
    Registered_User.username='{}' AND Registered_User.password='{}';
    """.format(username, password)

    cursor.execute(query)
    row = cursor.fetchall()

    if row == []:
        return False

    return  True

def get_item_byID(ID,type):
    query = """
    SELECT ID FROM {};
    """.format(type)
    cursor.execute(query)
    row = cursor.fetchall()

    for r in row:
        if r[0] == ID:
            query = """
            SELECT product.Quantity, product.Name FROM product WHERE product.ID='{}';
            """.format(ID)
            cursor.execute(query)
            row = cursor.fetchall()
            return row[0]

    return (-1,"-1")

def sortTuples( elementList, x = "ID"):
    dict = {"ID": 0, "Name": 1, "Quantity": 2, "InDate": 3, "OutDate": 4}
    stElement = dict[x]
    if stElement > 2:
        elementList.sort(key=operator.itemgetter(stElement), reverse=True)
    else:
        elementList.sort(key=operator.itemgetter(stElement))
