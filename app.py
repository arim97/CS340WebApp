
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import database.db_connector as db
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
    # Grab accounts data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the accounts in accounts table
        query = "SELECT account_id as ID, balance FROM Accounts"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_accounts page passing our query data to the edit_accounts template
        return render_template("account.j2", accounts=data)
    

    # Separate out the request methods, in this case this is for a POST
    # insert an account into the accounts entity
    if request.method == "POST":
        # fire off if user presses the Add Account button
        if request.form.get("Add_Account"):
            # grab user form inputs
            id = request.form["AccountID"]
            balance = request.form["balance"]
            query = "INSERT INTO Accounts (account_id , balance) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (id, balance))
            mysql.connection.commit()
            # redirect back to account page
            return redirect("/account")


# route for delete functionality, deleting an account from accounts,
# we want to pass the 'id' value of that account on button click (see HTML) via the route
@app.route("/delete_account/<int:id>")
def delete_account(id):
    # mySQL query to delete the account with our passed id
    query = "DELETE FROM Accounts WHERE account_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    # redirect back to accounts page
    return redirect("/account") 

# route for edit functionality, updating the attributes of an account in accounts
# similar to our delete route, we want to the pass the 'id' value of that account on button click (see HTML) via the route
@app.route("/edit_account/<int:id>", methods=["POST", "GET"])
def edit_accounts(id):
    if request.method == "GET":
        # mySQL query to grab the info of the account with our passed id
        query = "SELECT * FROM Accounts WHERE account_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        # render edit_accounts page passing our query data to the edit_accounts template
        return render_template("edit_account.j2", accounts=data)

    if request.method == "POST":
        # fire off if user clicks the 'Edit Account' button
        if request.form.get("Edit_Account"):
            # grab user form inputs
            id = request.form["accountID"]
            balance = request.form["balance"]
            query = "UPDATE Accounts SET Accounts.account_id = %s, Accounts.balance = %s WHERE Accounts.account_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (id, balance, id))
            mysql.connection.commit()
            # redirect back to account page after we execute the update query
            return redirect("/account")


# Transactions page route
@app.route('/transaction')
def Transactions():
    #query1 = "SELECT * FROM Transactions WHERE sender_id = %s OR destination_id = %s;"
    query1 = "SELECT * FROM Transactions;"
    cur = mysql.connection.cursor()
    cur.execute(query1)
    results = cur.fetchall()
    return render_template("transaction.j2", Transactions=results)

# Customers page route
@app.route('/customer', methods=["POST", "GET"])
def Customers():
    if request.method == "GET":
        query = "SELECT customer_id AS ID, name as Name, address AS Address, phone AS Phone, date_of_birth as DOB FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()
        print(results)
        return render_template("customer.j2", customers=results)

# Separate out the request methods, in this case this is for a POST
# insert an customer into the Customers entity
    if request.method == "POST":
        # fire off if user presses the Add Customer button
        if request.form.get("Add_Customer"):
            # grab user form inputs
            name = request.form["name"]
            address = request.form["address"]
            phone = request.form["phone"]
            dob = request.form["dob"]
            query = "INSERT INTO Customers (name, address, phone, date_of_birth ) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, address, phone, dob))
            mysql.connection.commit()
            # redirect back to customer page
            return redirect("/customer")

# Edit customer functionality
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
            name = request.form["name"]
            address = request.form["address"]
            phone = request.form["phone"]
            date_of_birth = request.form["date_of_birth"]
            query = "UPDATE Customers SET name = %s, address = %s, phone = %s, date_of_birth = %s WHERE customer_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, address, phone, date_of_birth, id))
            mysql.connection.commit()
            return redirect("/customer")
        
# Delete customer functionality       
@app.route("/delete_customers/<int:id>")
def delete_customer(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Customers WHERE customer_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    # redirect back to people page
    return redirect("/customer")



# Cards page route
@app.route('/cards',  methods=["POST", "GET"])
def Cards():
    # Grab cards data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the cards in cards table
        query = "SELECT * FROM Cards"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render cards page passing our query data to the edit_cards template
        return render_template("cards.j2", Cards=data)
    

    # Separate out the request methods, in this case this is for a POST
    # insert a card into the cards entity
    if request.method == "POST":
        # fire off if user presses the Add Account button
        if request.form.get("Add_Card"):
            # grab user form inputs
            card_id = request.form["card_id"]
            account_id= request.form["account_id"]
            scc = request.form["security_code"]
            exp_date = request.form["exp_date"]
            query = "INSERT INTO Cards (card_id , account_id, security_code, exp_date) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (card_id, account_id, scc, exp_date))
            mysql.connection.commit()
            # redirect back to account page
            return redirect("/cards")

# Delete card functionality
@app.route("/delete_card/<int:card_id>")
def delete_card(card_id):
    query = "DELETE FROM Cards WHERE card_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (card_id,))
    mysql.connection.commit()
    # redirect back to cards page
    return redirect("/cards") 

# Editing card functionality
@app.route("/edit_card/<int:card_id>", methods=["POST", "GET"])
def edit_card(card_id):
    if request.method == "GET":
        # mySQL query to grab the info of the account with our passed id
        query = "SELECT * FROM Cards WHERE card_id = %s" % (card_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        # render main card page passing our query data to the edit_cards template
        return render_template("card.j2", Cards=data)

    if request.method == "POST":
        # fire off if user clicks the 'Edit Account' button
        if request.form.get("Edit_Card"):
            # grab user form inputs
            card_id = request.form["card_id"]
            scc = request.form["security_code"]
            exp_date = request.form["exp_date"]
            query = "UPDATE Cards SET Cards.card_id = %s, Cards.security_code = %s, Cards.exp_date = %s WHERE Cards.card_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (card_id, scc, exp_date, card_id))
            mysql.connection.commit()
            # redirect back to account page after we execute the update query
            return redirect("/cards")

# Branches page route
@app.route('/branches',  methods=["POST", "GET"])
def Branches():
    # Grab branches data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the branches in branches table
        query = "SELECT * FROM Branches"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_branches page passing our query data to the branches template
        return render_template("branches.j2", Branches=data)
    

    # Separate out the request methods, in this case this is for a POST
    # insert an account into the branches entity
    if request.method == "POST":
        # fire off if user presses the Add Account button
        if request.form.get("Add_Branch"):
            # grab user form inputs
            branch_id = request.form["branch_id"]
            branch_name= request.form["branch_name"]
            address = request.form["address"]
            phone = request.form["phone"]
            manager = request.form["manager"]

            query = "INSERT INTO Branches (branch_id , branch_name, address, phone, manager) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (branch_id , branch_name, address, phone, manager))
            mysql.connection.commit()
            # redirect back to account page
            return redirect("/branches")

# Delete branch functionality
@app.route("/delete_branch/<int:branch_id>")
def delete_branch(branch_id):
    query = "DELETE FROM Branches WHERE branch_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (branch_id,))
    mysql.connection.commit()
    # redirect back to branches page
    return redirect("/branches") 

# Edit branch functionality
@app.route("/edit_branch/<int:branch_id>", methods=["POST", "GET"])
def edit_branch(branch_id):
    if request.method == "GET":
        # mySQL query to grab the info of the account with our passed id
        query = "SELECT * FROM Branches WHERE branch_id = %s" % (branch_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        # render edit_branches page passing our query data to the branches template
        return render_template("branch.j2", Branches=data)

    if request.method == "POST":
        # fire off if user clicks the 'Edit Branch' button
        if request.form.get("Edit_Branch"):
            # grab user form inputs
            branch_id = request.form["branch_id"]
            branch_name= request.form["branch_name"]
            address = request.form["address"]
            phone = request.form["phone"]
            manager = request.form["manager"]

            query = "UPDATE Branches SET Branches.branch_id = %s, Branches.branch_name = %s, Branches.address = %s, Branches.phone = %s, Branches.manager = %s WHERE Branches.branch_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (branch_id, branch_name, address, phone, manager, branch_id))
            mysql.connection.commit()
            # redirect back to branch page after we execute the update query
            return redirect("/branches")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 91115)) 

    
    app.run(port=port, debug=True) 

