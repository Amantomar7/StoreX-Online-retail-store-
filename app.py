from flask import Flask, render_template, redirect, request, session
import mysql.connector
from flask_mysqldb import MySQL
app = Flask(__name__)

# This key is for session which I have used to implement the user login feature
app.secret_key = 'SecretKey'

# This is sql connection 
def get_connection():
    return mysql.connector.connect(
        host="localhost", 
        user="----", #write user name here
        password="----", #write password of mysql here
        database="-----" #write database name here
    )


@app.route('/hello')
def hello_world():
    return 'Hello, World!'

#This is homepage route
@app.route('/')
def homepage():
    return render_template('homepage.html')

#This is for register all type's of users
@app.route('/register', methods = ['GET', 'POST'])
def UserType():
    if(request.method == 'POST'):
        User = request.form['RegisterRadio']
        if(User == 'customer'):
            return redirect('/registerCustomer')
        elif (User == 'supplier'):
            return redirect('/registerSupplier')
        else :
            return redirect('/registerDeliveryAgent')
    return render_template('UserType.html')

# This is login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        User = request.form['User Type']
        Email = request.form['Email']
        Password = request.form['Password']
        conn = get_connection()
        cursor = conn.cursor()
        if(User == 'customer'):
            cursor.execute("SELECT * FROM Customer WHERE Email = %s AND Hash_Password = %s", (Email, Password))
        elif (User == 'delivery Agent'):
            cursor.execute("SELECT * FROM DeliveryAgent WHERE Email = %s AND Hash_Password = %s", (Email, Password))
        else :
            cursor.execute("SELECT * FROM Supplier WHERE Email = %s AND Hash_Password = %s", (Email, Password))
            
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        # using connection here
        if user:
            session['user_id'] = user[0]
            session['user_type'] = User
            return redirect('/')
        else:
            return "wrong details"
    return render_template('login.html')

#for logout when user is logged in
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# This is register Page for customer
@app.route('/registerCustomer', methods = ['GET', 'POST'])
def registerCustomer():
    if(request.method == 'POST'):
        First_Name = request.form['First Name']
        Last_Name = request.form['Last Name']
        Age = request.form['Age']
        Email = request.form['Email']
        Phone = request.form['Phone']
        Address = request.form['Address']
        Pincode = request.form['Pincode']
        Password = request.form['Password']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Customer (FirstName, LastName, Email, Phone, Age, Hash_Password, Address, State_Pincode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (First_Name, Last_Name, Email, Phone, Age, Password, Address, Pincode))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/') #return to main site page
    return render_template('registerCustomer.html')

# This is register Page for supplier
@app.route('/registerSupplier', methods = ['GET', 'POST'])
def registerSupplier():
    if(request.method == 'POST'):
        Name = request.form['Name']
        Email = request.form['Email']
        Phone = request.form['Phone']
        Address = request.form['Address']
        Pincode = request.form['Pincode']
        Password = request.form['Password']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Supplier (SupplierName, Email, Phone, Hash_Password, Address, State_Pincode) VALUES (%s, %s, %s, %s, %s, %s)''', (Name, Email, Phone, Password, Address, Pincode))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')
    return render_template('registerSupplier.html')

# This is register Page for delivery agent
@app.route('/registerDeliveryAgent', methods = ['GET', 'POST'])
def registerDeliveryAgent():
    if(request.method == 'POST'):
        First_Name = request.form['First Name']
        Last_Name = request.form['Last Name']
        Email = request.form['Email']
        Phone = request.form['Phone']
        Address = request.form['Address']
        Pincode = request.form['Pincode']
        Password = request.form['Password']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO DeliveryAgent (FirstName, LastName, Email, Phone, Hash_Password, Address, State_Pincode) VALUES (%s, %s, %s, %s, %s, %s, %s)''', (First_Name, Last_Name, Email, Phone, Password, Address, Pincode))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')
    return render_template('registerDeliveryAgent.html')

#This is store where all product will be shown
@app.route('/store')
def store():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Product")  # Assuming your products table has a column named 'name'
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('store.html', products=products)

#This is cart 
@app.route('/cart')
def cart():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Cart")  # Assuming your products table has a column named 'name'
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('cart.html', products=products)

#This is choice page for buying or add to cart
@app.route('/choice')
def choice():
    return render_template('choice.html')

if __name__ == "__main__":
    app.run(debug = True)