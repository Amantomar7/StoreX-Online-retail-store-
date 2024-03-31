from flask import Flask, render_template, redirect, request, session
import mysql.connector
from flask_mysqldb import MySQL
from datetime import date
app = Flask(__name__)

# This key is for session which I have used to implement the user login feature
app.secret_key = 'Secret_key' #write any name here but use that every time you use this!

# This is sql connection 
def get_connection():
    return mysql.connector.connect(
        host="localhost", 
        user="root", #write user name here
        password="Aman", #write password of mysql here
        database="schemaall" #write database name here
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
        User = request.form['UserType']
        Email = request.form['Email']
        Password = request.form['Password']
        conn = get_connection()
        cursor = conn.cursor()
        if(User == 'customer'):
            cursor.execute("SELECT * FROM Customer WHERE Email = %s AND Hash_Password = %s", (Email, Password))
        elif (User == 'delivery_agent'):
            cursor.execute("SELECT * FROM DeliveryAgent WHERE Email = %s AND Hash_Password = %s", (Email, Password))
        elif(User == 'supplier'):
            cursor.execute("SELECT * FROM Supplier WHERE Email = %s AND Hash_Password = %s", (Email, Password))
        else :
            cursor.execute("SELECT * FROM SystemAdmin WHERE Email = %s AND Hash_Password = %s", (Email, Password))
            
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        # using connection here
        if user:
            session['user_id'] = user[0]
            session['user_type'] = User
            
            if(User == 'admin'):
                return redirect('/admin')
            elif(User == 'supplier'):
                return redirect('/supplier')
            elif(User == 'delivery_agent'):
                return redirect('/deliveryagent')
            else:
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
    cursor.execute("SELECT * FROM Product") 
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('store.html', products=products)

#This is cart 
@app.route('/cart')
def cart():
    conn = get_connection()
    cursor = conn.cursor()
    CustomerID = session['user_id']
    cursor.execute("SELECT c.ProductID, p.ProductName, c.Quantity, (c.Quantity * p.Price) as Total_Cost FROM Cart as c, Product as p Where c.ProductID = p.ProductID AND c.CustomerID = %s", (CustomerID,)) 
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('cart.html', products=products)

#This is choice page for buying or add to cart
# comes here from store using product Id as parameter
@app.route('/choice/<int:product_id>', methods=['GET'])
def choice(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Product WHERE ProductID = %s", (product_id,))
    product = cursor.fetchone() 
    print(product[0])
    cursor.close()
    conn.close()
    return render_template('choice.html', product=product)

@app.route('/account', methods=['POST', 'GET'])
def account():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to login if user is not logged in
    
    conn = get_connection()
    cursor = conn.cursor(buffered=True)
    if request.method == 'POST':
        amount = request.form['amount']
        cursor.execute("UPDATE Customer Set Balance = Balance + %s WHERE CustomerID = %s", (amount, session['user_id']))
    cursor.execute("SELECT * FROM Customer WHERE CustomerID = %s", (session['user_id'],))
    customer = cursor.fetchone()
    cursor.execute("""SELECT
                        MakeOrder.orderID, MakeOrder.OrderDate, Makeorder.DeliveryDate,
                        Product.ProductName, MakeOrder.Quantity, Product.Price,
                        (Makeorder.Quantity * Product.Price) AS total_price,
                    CASE
	                    WHEN (MakeOrder.Deliverydate IS NULL) = True THEN 'Not Delivered'
	                    ELSE 'Delivered'
                    END AS delivered
                    FROM 
                        MakeOrder
                    INNER JOIN 
                        Product ON MakeOrder.ProductID = Product.ProductID and MakeOrder.OrderStatus = %s
                    WHERE 
                        MakeOrder.CustomerID = %s
                    ORDER BY 
                        Makeorder.OrderDate;""",('Done', session['user_id']))
    product_history = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('account.html', customer=customer, product_history = product_history)

@app.route('/addbalance')
def addbalance():
    return render_template('addbalance.html')

# This is for pay or buy page 
# comes here from choice using product_id as parameter
@app.route('/buy_now/<int:product_id>', methods = ['GET', 'POST'])
def buy_now(product_id):
    # this is customer ID session['user_id']
    # now need product Id which has been chosen 
    conn = get_connection()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM Customer Where CustomerID = %s", (session['user_id'],))
    customer = cursor.fetchone()
    cursor.execute("SELECT * FROM Product WHERE ProductID = %s", (product_id,))
    product = cursor.fetchone() 
    cursor.close()
    conn.close()
    if(customer[8] < product[2]):
        return "Not enough Balance GO to Account's"
    return render_template('purchase.html', product=product)

# This is thank you page 
# comes here after clicking [ pay ] in buy now page
@app.route('/purchased/<int:product_id>', methods = ['GET', 'POST'])
def purchased(product_id):
    
    conn = get_connection()
    cursor = conn.cursor(buffered = True)
    cursor.execute("SELECT * from DeliveryAgent Where Availability = %s", (0,))
    DeliveryID = cursor.fetchone()[0]
    CustomerID = session['user_id']
    if request.method == 'POST':
        cursor.execute("INSERT INTO MAKEORDER (CustomerID, DeliveryID, ProductId, Quantity, OrderStatus, OrderDate) VALUES (%s, %s, %s, %s, %s, %s)",
                       (CustomerID, DeliveryID, product_id, 1, "Done", date.today()))
        conn.commit()
    print(DeliveryID)
    print(product_id)
    cursor.close()
    conn.close()
    return render_template('thankyou.html', product_id=product_id)

# This is thank you page
# for returning to home page
@app.route('/go_to_home', methods = ['GET', 'POST'])
def go_to_home():
    # this is customer ID session['user_id']
    # now need product Id which has been chosen 
    if(request.method == 'POST'):
        return redirect('/store')
    return render_template('thankyou.html')


# checcking for searched item's
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        query = request.args.get('query')
        conn = get_connection()
        cursor = conn.cursor()
        # taking all products matching searched result
        cursor.execute(f"SELECT * FROM Product WHERE ProductName LIKE '%{query}%'")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('search.html', products=products)
    else:
        return render_template('search.html')

# inserting into cart
@app.route('/added_to_cart/<int:product_id>', methods = ['GET', 'POST'])
def add_to_cart(product_id):
    # this is customer ID session['user_id']
    # now need product Id which has been chosen 
    conn = get_connection()
    cursor = conn.cursor()
    CustomerID = session['user_id']
    if(request.method == 'POST'):
        cursor.execute("INSERT INTO Cart (CustomerID, ProductID, Quantity) Values (%s, %s, %s)", (CustomerID, product_id, 1))
        conn.commit()
    cursor.close()
    conn.close()
    return render_template('added_to_cart.html', product_id = product_id) 


# admin page for various stats
@app.route('/admin')
def admin():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(CustomerID) FROM Customer")
    # Total customer registered
    customer_count = cursor.fetchone()
    cursor.execute("SELECT COUNT(SupplierID) FROM Supplier")
    # Total supplier registered
    supplier_count = cursor.fetchone()
    cursor.execute("SELECT COUNT(DeliveryID) FROM DeliveryAgent")
    # Total delivery Agent registered
    deliveryAgent_count = cursor.fetchone()
    cursor.execute("SELECT COUNT(OrderID) FROM MakeOrder")
    # Total order's registered
    order_count = cursor.fetchone()
    cursor.execute("SELECT COUNT(ProductID) FROM Product")
    # Total product registered
    product_count = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('admin.html', customer_count=customer_count, supplier_count=supplier_count, deliveryAgent_count = deliveryAgent_count, order_count=order_count, product_count=product_count) 

@app.route('/customerstats')
def customer_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT 
                        mo.CustomerID,
                        c.FirstName,
                        c.LastName,
                    SUM(p.Price * mo.Quantity) AS TotalPurchaseAmount
                FROM 
                    MakeOrder mo
                JOIN 
                    Customer c ON mo.CustomerID = c.CustomerID
                JOIN
                    Product p ON mo.ProductID = p.ProductID
                WHERE 
                    mo.OrderStatus = %s
                GROUP BY 
                    mo.CustomerID,
                    c.FirstName,
                    c.LastName
                ORDER BY 
                    TotalPurchaseAmount DESC
                LIMIT %s""", ('Done', 3))
    top_customer = cursor.fetchall()
    print(top_customer[0][1])
    # Gold membership customer's
    cursor.execute("""Select 
                        mo.OrderID,
                        mo.OrderDate
                    FROM 
                        MakeOrder mo
                    JOIN 
                        Customer c ON mo.CustomerID = c.CustomerID
                    WHERE 
                        c.MembershipStatus = %s
                        AND mo.OrderStatus = %s
                    LIMIT %s""", ('Gold', 'Done', 3))
    gold_customer = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('customerstats.html', top_customer=top_customer, gold_customer=gold_customer) 


@app.route('/productstats')
def product_stats():
    return render_template('productstats.html')

@app.route('/supplierstats')
def supplier_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""""")
    
    cursor.close()
    conn.close()
    return render_template('supplierstats.html')

@app.route('/orderstats')
def order_stats():
    conn = get_connection()
    cursor = conn.cursor(buffered=True)
    # Total revenue
    cursor.execute("""SELECT SUM(sub.total_price) AS total_sum
                        FROM (
                                SELECT p.Price * m.Quantity AS total_price
                                FROM Product p
                                INNER JOIN MakeOrder m ON p.ProductID = m.ProductID and m.OrderDate = %s
                            ) AS sub""", (date.today(),))
    revenue = cursor.fetchone()
    # now for profit
    cursor.execute("""SELECT 
                            SUM((p.Price - s.PricePerProduct) * m.Quantity) AS TotalProfit
                        FROM 
                            MakeOrder m
                        INNER JOIN 
                            Product p ON m.ProductID = p.ProductID
                        INNER JOIN 
                            Sells s ON p.SupplierID = s.SupplierID AND p.ProductID = s.ProductID
                        WHERE 
                            m.OrderDate = %s""", (date.today(),))
    profit = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('orderstats.html', revenue = revenue, profit = profit)

@app.route('/deliveryagentstats')
def delivery_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""""")
    
    cursor.close()
    conn.close()
    return render_template('deliveryagentstats.html')


# let's make a page for supplier to add product into the 
@app.route('/supplier')
def supplier():
    conn = get_connection()
    cursor = conn.cursor(buffered = True)
    cursor.execute("""SELECT * FROM SUPPLIER WHERE SupplierID = %s""", (session['user_id'],))
    user = cursor.fetchone()
    cursor.execute("""SELECT p.ProductID, p.ProductName, s.Quantity, (s.Quantity * s.PricePerProduct) as Revenue, s.PricePerProduct
                    FROM 
                        PRODUCT as p 
                    INNER JOIN 
                        SELLS as s 
                    Where 
                        p.ProductID = s.ProductID and s.SupplierID = %s""", (session['user_id'],))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('supplier.html', user = user, products = products)

# this is for home page for delivery agent
@app.route('/deliveryagent')
def deliveryagent():
    conn = get_connection()
    cursor = conn.cursor(buffered = True)
    # query for getting all orders
    cursor.execute("""SELECT * FROM DeliveryAgent Where DeliveryID = %s""", (session['user_id'],))
    orders = cursor.fetchone()
    # query for all delivered orders
    cursor.execute("""SELECT * FROM SELLS WHERE SupplierID = %s""", (session['user_id'],))
    completed_orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('deliveryagent.html')

@app.route('/all_customer')
def all_customer():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Customer""")
    all_Customer = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('allcustomer.html', all_Customer = all_Customer)

@app.route('/all_supplier')
def all_supplier():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Supplier""")
    all_Supplier = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('allsupplier.html', all_Supplier = all_Supplier)

@app.route('/all_products')
def all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Product""")
    all_Products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('allproducts.html', all_Products = all_Products)

@app.route('/all_deliveryagent')
def all_deliveryagent():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM DeliveryAgent""")
    all_Deliveryagent = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('alldeliveryagent.html', all_Deliveryagent = all_Deliveryagent)

@app.route('/all_orders')
def all_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT m.OrderID, m.CustomerID, m.ProductID, m.DeliveryID, m.Quantity, m.Orderstatus, m.OrderDate, p.ProductName, (p.Price * m.Quantity) as Price
                        FROM 
                            product as p
                        INNER JOIN 
                            MakeOrder as m ON p.ProductID = m.ProductID""")
    all_Orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('all_orders.html', all_Orders = all_Orders)


if __name__ == "__main__":
    app.run(debug = True)
    
    
#making of triggers