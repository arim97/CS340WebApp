from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_arim'
app.config['MYSQL_PASSWORD'] = 'DlkI86YvGvtb' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_arim'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
mysql = MySQL(app)

# Routes 

# Homepage route
@app.route('/')
def root():
    return render_template("main.j2")

# Accounts page route
@app.route('/account',  methods=["POST", "GET"])
def Accounts():
    query1 = "SELECT account_id AS 'Account No.' , balance AS Balance FROM Accounts ;"
    query2 = "SELECT * FROM Cards;"
    cur = mysql.connection.cursor()
    cur.execute(query1)
    results = cur.fetchall()
    cur.execute(query2)
    return render_template("account.j2", Accounts=results)
# Transactions page route
@app.route('/transaction/<int:id>', methods=["POST", "GET"])
def Transactions(id):
    if request.method == "GET":
        query1 = "SELECT * FROM Transactions WHERE sender_id = %s OR destination_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query1, (id, id))
        results = cur.fetchall()
        return render_template("transaction.j2", Transactions=results)

# Customers page route
@app.route('/customer')
def Customers():
    query = "SELECT * FROM Customers;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template("customer.j2", customer=results)
@app.route("/edit_customers/<int:id>", methods=["POST", "GET"])
def edit_customers(id):
    if request.method == "GET":
        query = "SELECT * FROM Customers WHERE customer_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_customers.j2", customer=data)

    if request.method == "POST":
        if request.form.get("Edit_Customer"):
            customer_id = request.form["customerID"]
            name = request.form["name"]
            address = request.form["address"]
            phone = request.form["phone"]
            date_of_birth = request.form["date_of_birth"]

            query = "UPDATE Customers SET name = %s, address = %s, phone = %s, date_of_birth = %s WHERE customer_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, address, phone, date_of_birth, customer_id))
            mysql.connection.commit()

            return redirect("/customer")

# Cards page route
@app.route('/card')
def Cards():
    query = "SELECT * FROM Cards;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template("card.j2", Cards=results)

# Branches page route
@app.route('/branch')
def Branches():
    query = "SELECT * FROM Branches;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template("branch.j2", Branches=results)


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 55233)) 
    
    app.run(port=port, debug=True) 

