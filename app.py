from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import database.db_connector as db
import os
db_connection = db.connect_to_database()
app = Flask(__name__,template_folder='templates')

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
    return render_template("account.j2", accounts=results)
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

@app.route('/cards', methods=['GET', 'POST'])
def cards():
    if request.method == 'POST':
        card_id = request.form.get('card_id') 
        account_id = request.form.get('account_id')
        scc = request.form.get('security_code')
        exp_date = request.form.get('exp_date')
        
        query = "INSERT INTO Cards (card_id, account_id, security_code, exp_date) VALUES (%s, %s, %s, %s);"
        db.execute_query(db_connection=db_connection, query=query, query_params=(card_id, account_id, scc, exp_date))
        return redirect('/cards')

    query = "SELECT * FROM Cards;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("cards.j2", Cards=results)

@app.route('/delete_card/<int:card_id>', methods=['GET', 'POST'])
def delete_card(card_id): 
    query = "DELETE FROM Cards WHERE card_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(card_id,))
    return redirect('/cards')

@app.route('/cards/<int:card_id>', methods=['GET', 'POST', 'DELETE'])
def card(card_id):
    if request.method == 'POST':
        card_id = request.form.get('card_id') 
        account_id = request.form.get('account_id')
        scc = request.form.get('security_code')
        exp_date = request.form.get('exp_date')
        
        query = "UPDATE Cards SET account_id = %s,security_code = %s, exp_date = %s WHERE card_id = %s;"
        db.execute_query(db_connection=db_connection, query=query, query_params=(account_id, scc, exp_date, card_id))

    elif request.method == 'DELETE':
        query = "DELETE FROM Cards WHERE card_id = %s;"
        db.execute_query(db_connection=db_connection, query=query, query_params=(card_id,))
        
    query = "SELECT * FROM Cards WHERE card_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(card_id,))
    result = cursor.fetchone()
    return render_template("card.j2", Cards=result)  # Render a specific template for individual patient

# Branches page route
@app.route('/branches', methods=['GET', 'POST'])
def branches():
    if request.method == 'POST':
        branch_id = request.form.get('branch_id') 
        branch_name = request.form.get('branch_name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        manager = request.form.get('manager')
        
        query = "INSERT INTO Branches (branch_id, branch_name, address, phone, manager) VALUES (%s, %s, %s, %s, %s);"
        db.execute_query(db_connection=db_connection, query=query, query_params=(branch_id, branch_name, address, phone, manager))
        return redirect('/branches')

    query = "SELECT * FROM Branches;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("branches.j2", Branches=results)

@app.route('/delete_branch/<int:branch_id>', methods=['GET', 'POST'])
def delete_branch(branch_id): 
    query = "DELETE FROM Branches WHERE branch_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(branch_id,))
    return redirect('/branches')

@app.route('/branches/<int:branch_id>', methods=['GET', 'POST', 'DELETE'])
def branch(branch_id):
    if request.method == 'POST':
        branch_id = request.form.get('branch_id') 
        branch_name = request.form.get('branch_name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        manager = request.form.get('manager')
        
        query = "UPDATE Branches SET branch_name = %s,address = %s, phone = %s, manager = %s WHERE branch_id = %s;"
        db.execute_query(db_connection=db_connection, query=query, query_params=(branch_name, address, phone, manager, branch_id))

    elif request.method == 'DELETE':
        query = "DELETE FROM Branches WHERE branch_id = %s;"
        db.execute_query(db_connection=db_connection, query=query, query_params=(branch_id,))
        
    query = "SELECT * FROM Cards WHERE card_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(branch_id,))
    result = cursor.fetchone()
    return render_template("branch.j2", Branch=result)  # Render a specific template for individual patient


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 55233)) 

    
    app.run(port=port, debug=True) 

