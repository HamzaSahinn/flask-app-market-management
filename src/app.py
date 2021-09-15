from flask import Flask, render_template, request, redirect, session, url_for
from connect import cursor, cnx
from datetime import datetime
from Utils import generate_product_id, generate_out_log_id, generate_in_log_id, is_unqiue, get_item_byID, check_user, sortTuples
import operator


def addNewItem(item_id, new_item):
    stmt = """INSERT INTO product (ID, Name, Quantity) VALUES (%s, %s, %s);"""
    data = (item_id, new_item["Name"], int(new_item["Quantity"]))
    cursor.execute(stmt, data)

    stmt = """INSERT INTO {} (ID, Name, Quantity) VALUES (%s, %s, %s);""".format(db_list[new_item["Type"]])
    data = (item_id, new_item["Name"], int(new_item["Quantity"]))
    cursor.execute(stmt, data)

    stmt = """INSERT INTO In_log(ID, Name, In_Date, EUD, In_Quantity, In_Log_ID, Price) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    InDate = datetime.today().strftime('%Y-%m-%d')

    data = (item_id, new_item["Name"], InDate, new_item["EUD"], int(new_item["Quantity"]), generate_in_log_id(),
            float(new_item["Price"]))

    if(new_item["EUD"] == ''):
        data = (item_id, new_item["Name"], InDate, "0000-00-00", int(new_item["Quantity"]), generate_in_log_id(),
                float(new_item["Price"]))

    cursor.execute(stmt, data)
    cnx.commit()

def updateInItem(isID, new_item):
    newQuan = isID[1] + int(new_item["Quantity"])
    stmt = "UPDATE {} SET Quantity = %s WHERE ID = %s".format(db_list[new_item["Type"]])
    data = (newQuan, isID[0])
    cursor.execute(stmt, data)

    stmt = "UPDATE product SET Quantity = %s WHERE ID = %s"
    data = (newQuan, isID[0])
    cursor.execute(stmt, data)

    stmt = """INSERT INTO In_log(ID, Name, In_Date, EUD, In_Quantity, In_Log_ID, Price) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    InDate = datetime.today().strftime('%Y-%m-%d')
    data = (isID[0], new_item["Name"], InDate, new_item["EUD"], int(new_item["Quantity"]), generate_in_log_id(),
            float(new_item["Price"]))

    if(new_item["EUD"] == ''):
        data = (isID[0], new_item["Name"], InDate, "0000-00-00", int(new_item["Quantity"]), generate_in_log_id(),
                float(new_item["Price"]))

    cursor.execute(stmt, data)
    cnx.commit()

def updateOutItem(new_item, item):
    newQuan = int(item[0]) - int(new_item["Quantity"])

    stmt = """UPDATE {} SET Quantity = %s WHERE ID = %s""".format(db_list[new_item["Type"]])
    data = (newQuan, new_item["ID"])
    cursor.execute(stmt, data)
    r = cursor.rowcount

    if r != 0: #IF there is an element and all the gicen information is correct
        stmt = """UPDATE product SET Quantity = %s WHERE ID = %s"""
        data = (newQuan, new_item["ID"])
        cursor.execute(stmt, data)

        stmt = """INSERT INTO Out_log(ID, Name, Out_Quantity, Out_Date, Out_Log_ID) VALUES (%s, %s, %s, %s, %s);"""
        OutDate = datetime.today().strftime('%Y-%m-%d')
        data = (new_item["ID"], item[1], new_item["Quantity"], OutDate, generate_out_log_id())
        cursor.execute(stmt, data)
        cnx.commit()
    else:
        cnx.commit()
def getCountsAndQuantities():
    cursor.execute("SELECT COUNT(*) FROM houseware;")
    hwC = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM cleaning;")
    clC = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM food_drink;")
    fdC = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM other;")
    otC = cursor.fetchall()

    cursor.execute("SELECT SUM(Quantity) FROM houseware")
    hwS = cursor.fetchall()
    cursor.execute("SELECT SUM(Quantity) FROM cleaning")
    clS = cursor.fetchall()
    cursor.execute("SELECT SUM(Quantity) FROM food_drink")
    fdS = cursor.fetchall()
    cursor.execute("SELECT SUM(Quantity) FROM other")
    otS = cursor.fetchall()

    return [(hwC[0][0], clC[0][0], fdC[0][0], otC[0][0]), (int(hwS[0][0]), int(clS[0][0]), int(fdS[0][0]), int(otS[0][0]))]


app = Flask(__name__)
cursor.execute("USE {}".format("supermarketdb"))
db_list = {"Food/Drink":"food_drink", "Cleaning":"cleaning", "Houseware":"houseware", "Other":"other"}

@app.route('/')
def root():
    return render_template("login_page.html")

@app.route("/login_page")
def login_page():
    err = request.args["message"]
    return  render_template("login_page.html", err=err)

@app.route("/loginUser", methods=["POST"])
def loginUser():
    new_item = request.form
    username = new_item["Username"]
    password = new_item["Password"]
    is_registered = check_user(username, password)
    if(is_registered):
        return redirect("mainpage")
    else:
        message = "Username or Password Incorrect"
        return redirect(url_for('.login_page', message=message))

@app.route("/mainpage")
def main_page():
    dashboard = getCountsAndQuantities()
    return render_template("mainpage.html", dash0 = dashboard[0], dash1 = dashboard[1])

@app.route("/mainpageError")
def main_pageE():
    dashboard = getCountsAndQuantities()
    err = request.args["errMain"]
    return render_template("mainpage.html", dash0 = dashboard[0], dash1 = dashboard[1], err = err)

@app.route("/addItem", methods=["POST"])
def addItem():
    new_item = request.form
    isID = is_unqiue(new_item["Name"])
    if isID[0] == -1:
        item_id = generate_product_id()
        addNewItem(item_id, new_item)
        return redirect("mainpage")
    else:
        updateInItem(isID, new_item)
        return redirect("mainpage")

@app.route("/outItem", methods=["POST"])
def outItem():
    new_item = request.form
    item = get_item_byID(int(new_item["ID"]), db_list[new_item["Type"]])
    if int(item[0]) == -1 or item[0] < int(new_item["Quantity"]):
        message = "Wrong ID, Type or Quantity"
        return redirect(url_for('.main_pageE', errMain=message))
    else:
        updateOutItem(new_item, item)
        return redirect("mainpage")

@app.route("/FoodDrink")
def foodDrink():
    cursor.execute("SELECT * FROM food_drink")
    all_rows = cursor.fetchall()
    sortTuples(all_rows,"Name")
    return render_template("FoodDrink.html", all_rows = all_rows)

@app.route("/Housware")
def Houseware():
    cursor.execute("SELECT * FROM houseware")
    all_rows = cursor.fetchall()
    sortTuples(all_rows, "Name")
    return render_template("Housware.html", all_rows = all_rows)

@app.route("/InLog")
def InLog():
    cursor.execute("SELECT * FROM in_log")
    all_rows = cursor.fetchall()
    sortTuples(all_rows, "InDate")
    return render_template("InLog.html", all_rows = all_rows)

@app.route("/InLogSortByName")
def InLogSortByName():
    cursor.execute("SELECT * FROM in_log")
    all_rows = cursor.fetchall()
    sortTuples(all_rows, "Name")
    return render_template("InLog.html", all_rows = all_rows)

@app.route("/OutLog")
def OutLog():
    cursor.execute("SELECT * FROM out_log")
    all_rows = cursor.fetchall()
    sortTuples(all_rows, "OutDate")
    return render_template("OutLog.html", all_rows = all_rows)

@app.route("/OutLogSortByName")
def OutLogSortByName():
    cursor.execute("SELECT * FROM out_log")
    all_rows = cursor.fetchall()
    sortTuples(all_rows, "Name")
    return render_template("OutLog.html", all_rows = all_rows)

@app.route("/Other")
def Other():
    cursor.execute("SELECT * FROM other")
    all_rows = cursor.fetchall()
    sortTuples(all_rows, "Name")
    return render_template("Other.html",  all_rows = all_rows)

@app.route("/CleaningMaterial")
def CleaningMaterial():
    cursor.execute("SELECT * FROM cleaning")
    all_rows = cursor.fetchall()
    sortTuples(all_rows, "Name")
    return render_template("CleaningMaterial.html",  all_rows = all_rows)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run()
