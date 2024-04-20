from flask import Flask, render_template, redirect, request, session
import mysql.connector
from flask_mysqldb import MySQL
from datetime import *
import threading
app = Flask(__name__)

# This key is for session which I have used to implement the user login feature
app.secret_key = 'Secret_key' #write any name here but use that every time you use this!

# This is sql connection 
def get_connection():
    return mysql.connector.connect(
        host="localhost", 
        user="root", #write user name here
        password="Aman", #write password of mysql here
        database="schema_1" #write database name here
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
            # adding user in session for using who is logged in
            session['user_id'] = user[0]
            session['user_type'] = User
            # redirecting respective user to respective page
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
        try:
            # execcuting the mysql statement
            cursor.execute('''INSERT INTO Customer (FirstName, LastName, Email, Phone, Age, Hash_Password, Address, State_Pincode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (First_Name, Last_Name, Email, Phone, Age, Password, Address, Pincode))
            # commiting into the database
            conn.commit()
        except mysql.connector.Error as err:
            # if any error occur then rollback to the start of the transaction
            conn.rollback()
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


@app.route('/changeprofile', methods = ['GET', 'POST'])
def changeprofile():
    return render_template('changeprofile.html')

@app.route('/changeaccount', methods = ['GET', 'POST'])
def changeaccount():
    if(request.method == 'POST'):
        customerID = session['user_id']
        firstname = request.form['First Name']
        lastname = request.form['Last Name']
        age = request.form['Age']
        email = request.form['Email']
        address = request.form['Address']
        pincode = request.form['Pincode']
        phone = request.form['Phone']
        password = request.form['Password']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""UPDATE Customer SET FirstName = %s, LastName = %s, Age = %s, Email = %s, Phone = %s, Address = %s, State_Pincode = %s, Hash_Password = %s WHERE customerID = %s""", (firstname, lastname, age, email, phone, address, pincode, password, customerID))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect('/')

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

#This is cart for the given customer
@app.route('/cart')
def cart():
    conn = get_connection()
    cursor = conn.cursor()
    CustomerID = session['user_id']
    cursor.execute("SELECT c.ProductID, p.ProductName, c.Quantity, (c.Quantity * p.Price) as Total_Cost, c.CartID FROM Cart as c, Product as p Where c.ProductID = p.ProductID AND c.CustomerID = %s", (CustomerID,)) 
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('cart.html', products=products)

# This is choice page for buying or add to cart
# comes here from store using product Id as parameter
@app.route('/choice/<int:product_id>', methods=['GET'])
def choice(product_id):
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Product WHERE ProductID = %s", (product_id,))
    product = cursor.fetchone() 
    cursor.close()
    conn.close()
    return render_template('choice.html', product=product)

# This is for account page of the Customer
@app.route('/account', methods=['POST', 'GET'])
def account():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to login if user is not logged in
    conn = get_connection()
    cursor = conn.cursor(buffered=True)
    if request.method == 'POST':
        amount = request.form['amount']
        cursor.execute("UPDATE Customer Set Balance = Balance + %s WHERE CustomerID = %s", (amount, session['user_id']))
        conn.commit()
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

# for rendering page of adding balance for the customer
@app.route('/addbalance')
def addbalance():
    return render_template('addbalance.html')

# This is for pay or buy page 
# comes here from choice using product_id as parameter
@app.route('/buy_now/<int:product_id>', methods = ['GET', 'POST'])
def buy_now(product_id):
    # this is customer ID session['user_id']
    # now need product Id which has been chosen 
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_connection()
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT * FROM Customer Where CustomerID = %s", (session['user_id'],))
    customer = cursor.fetchone()
    cursor.execute("SELECT * FROM Product WHERE ProductID = %s", (product_id,))
    product = cursor.fetchone() 
    cursor.close()
    conn.close()
    if(product[5] <= 0):
        return "NOT IN STOCK!"
    # checking for enough balance 
    if(customer[8] < product[2]):
        return "Not enough Balance GO to Account's"
    return render_template('purchase.html', product=product)

# This is thank you page 
# comes here after clicking [ pay ] in buy now page
@app.route('/purchased/<int:product_id>', methods = ['GET', 'POST'])
def purchased(product_id):
    
    conn = get_connection()
    cursor = conn.cursor(buffered = True)
    cursor.execute("SELECT Quantity FROM Product WHERE PRODUCTID = %s", (product_id,))
    products = cursor.fetchone()
    if(products[0] <= 0):
        return "NOT IN STOCK!"
    cursor.execute("SELECT * from DeliveryAgent Where Availability = %s", (0,))
    if request.method == 'POST':
        try:  
            DeliveryID = cursor.fetchone()[0]
            CustomerID = session['user_id']
            cursor.execute("INSERT INTO MAKEORDER (CustomerID, DeliveryID, ProductId, Quantity, OrderStatus, OrderDate) VALUES (%s, %s, %s, %s, %s, %s)",
                        (CustomerID, DeliveryID, product_id, 1, "Done", date.today()))
            cursor.execute("UPDATE PRODUCT set Quantity = Quantity - %s", (1,))
            conn.commit()
        except mysql.connector.Error as err:
            conn.rollback()
    # print(DeliveryID)
    # print(product_id)
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

# for removing item in product
@app.route('/remove/<int:product_id>', methods = ['GET', 'POST'])
def remove(product_id):
    conn = get_connection()
    cursor = conn.cursor(buffered = True)
    cursor.execute("DELETE from CART Where CartID = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/cart')

# showing all delivery agent stats in this page
@app.route('/product_details/<int:product_id>')
def product_details(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT p.ProductName, p.price, p.Quantity, p.ProductDescription, c.CategoryName, p.ProductID 
                        FROM 
                            Product AS p
                        INNER JOIN
                            Category AS c
                        WHERE 
                            c.CategoryID = p.CategoryID AND p.ProductID = %s""", (product_id,))
    details = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('productdetails.html', details = details)


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

# showing all customer stats in this page
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
                    mo.OrderStatus = %s AND c.MembershipStatus = %s
                GROUP BY 
                    mo.CustomerID,
                    c.FirstName,
                    c.LastName
                ORDER BY 
                    TotalPurchaseAmount DESC
                LIMIT %s""", ('Done', 'Gold', 3))
    gold_customer = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('customerstats.html', top_customer=top_customer, gold_customer=gold_customer) 

# showing all products stats in this page
@app.route('/productstats')
def product_stats():
    return render_template('productstats.html')

# showing all supplier stats in this page
@app.route('/supplierstats')
def supplier_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""""")
    
    cursor.close()
    conn.close()
    return render_template('supplierstats.html')

# showing all order stats in this page / showing profit and revenue
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

# showing all delivery agent stats in this page
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

# for getting to the page of the adding product for the supplier
@app.route('/getSupplier', methods = ['POST', 'GET'])
def getSupplier():
    return render_template('addproductSupplier.html')
    


# for adding product into the sells table and make that working the product table
@app.route('/addproductSupplier', methods = ['POST', 'GET'])
def addproductSupplier():
    if(request.method == 'POST'):
        supplier_id = session['user_id']
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        priceper_product = request.form['price_per_product']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT count(*) FROM SELLS WHERE SupplierId = %s AND ProductId = %s""", (supplier_id, product_id))
        have = cursor.fetchall()[0][0]
        print(have)
        try:
            if(have):
                cursor.execute("""UPDATE SELLS SET Quantity = Quantity + %s, PricePerProduct = %s WHERE SupplierId = %s AND ProductID = %s""", (quantity, priceper_product, supplier_id, product_id))
            else :
                cursor.execute("""INSERT INTO SELLS (SupplierID, ProductID, Quantity, PricePerProduct) VALUES(%s, %s, %s, %s)""", (supplier_id, product_id, quantity, priceper_product))
            # making change in the product table as well
            cursor.execute("""UPDATE Product SET Quantity = Quantity + %s WHERE ProductID = %s AND SupplierID = %s""", (quantity, product_id, supplier_id))
            conn.commit()
        except mysql.connector.Error as err:
            conn.rollback()
        cursor.close()
        conn.close()
    return render_template('thanksforsupplier.html')

# this is for home page for delivery agent
@app.route('/deliveryagent')
def deliveryagent():
    conn = get_connection()
    cursor = conn.cursor(buffered=True)
    cursor.execute("""SELECT c.CustomerID, CONCAT(c.FirstName, " ", c.LastName) as CustomerName, c.Phone, o.OrderID, o.OrderDate, o.ProductID
                        FROM 
                            MakeOrder as o
                        INNER JOIN
                            Customer as c
                        Where 
                            c.CustomerID = o.CustomerID AND o.DeliveryID = %s AND DeliveryDate IS NULL""", (session['user_id'],))
    active_orders = cursor.fetchall()
    cursor.execute("""SELECT OrderID, ProductID, DeliveryDate, CustomerID FROM MakeOrder WHERE DeliveryID = %s AND DeliveryDate IS NOT NULL""", (session['user_id'],))
    delivered_orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('deliveryagent.html', active_orders = active_orders, delivered_orders = delivered_orders)


@app.route('/delivered/<int:order_id>')
def delivered(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE MakeOrder SET DeliveryDate = %s WHERE OrderID = %s", (date.today(), order_id))
    conn.commit()
    cursor.execute("UPDATE DeliveryAgent SET Availability = %s WHERE DeliveryID = %s", (0, session['user_id']))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/deliveryagent')


# page for all customer stats
@app.route('/all_customer')
def all_customer():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT CustomerId, CONCAT(FirstName, " ", LastName), MembershipStatus, Email, Phone FROM Customer""")
    all_Customer = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('allcustomer.html', all_Customer = all_Customer)



# page for all customer stats
@app.route('/removecustomer/<int:customer_id>')
def removecustomer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    # customer with customer_id is deleted
    try:
        cursor.execute("""DELETE FROM Customer WHERE CustomerID = %s""", (customer_id,))
        # delete from orders
        cursor.execute("""DELETE FROM MakeOrder WHERE CustomerID = %s""", (customer_id,))
        # delete from product rating
        cursor.execute("""DELETE FROM ProductReview WHERE CustomerID = %s""", (customer_id,))
        # delete from agent review
        cursor.execute("""DELETE FROM AgentReview WHERE CustomerID = %s""", (customer_id,))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
    cursor.close()
    conn.close()
    return redirect('/all_customer')

# page for all supplier page
@app.route('/all_supplier')
def all_supplier():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Supplier""")
    all_Supplier = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('allsupplier.html', all_Supplier = all_Supplier)

# page of all products
@app.route('/all_products')
def all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Product""")
    all_Products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('allproducts.html', all_Products = all_Products)

# page for all delivery agent
@app.route('/all_deliveryagent')
def all_deliveryagent():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT DeliveryID, CONCAT(FirstName, " ", LastName) as Name, Email, 
                        CASE
                            WHEN Availability = %s THEN %s
                            ELSE %s
                        END AS Avail
                   FROM DeliveryAgent""", (1, 'Not Available', 'Available'))
    all_Deliveryagent = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('alldeliveryagent.html', all_Deliveryagent = all_Deliveryagent)

# for all orders page 
@app.route('/deliveryrating')
def deliverrating():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT d.DeliveryID, CONCAT(FirstName, " ", LastName) as fullname ,AVG(r.Rating) as AverageRating
                        FROM 
                            DeliveryAgent as d
                        Inner JOIN 
                            AgentReview as r
                        Where 
                            d.DeliveryID = r.DeliveryID
                        GROUP By 
                            d.DeliveryID, fullname;""")
    allrating = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('deliveryrating.html', allrating = allrating)

# for all orders page 
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

# this is for getting product number into the product_review function
@app.route('/product_number/<int:order_id>', methods = ['POST', 'GET'])
def product_number(order_id):
    print(order_id)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * From MakeOrder Where OrderID = %s""", (order_id,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('productreview.html', order = order)

@app.route('/product_number_for_delivery/<int:order_id>', methods = ['POST', 'GET'])
def product_number_for_delivery(order_id):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MakeOrder WHERE OrderId = %s AND DeliveryDate IS NOT NULL", (order_id,))
    total_order = cursor.fetchall()
    if(len(total_order) == 0):
        return "Product has not delivered yet!" 
    cursor.execute("""SELECT * From MakeOrder Where OrderID = %s""", (order_id,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('deliveryreview.html', order = order)



# for inserting review of product into the table
@app.route('/product_review/<int:order_id>', methods = ['POST', 'GET'])
def product_review(order_id):
    if(request.method == 'POST'):
        Rating = request.form['Rating']
        Desc = request.form['Desc']
        customerID = session['user_id']
        conn = get_connection()
        cursor = conn.cursor()
        # insert into the rating table
        cursor.execute("""SELECT ProductID from MAKEORDER WHERE OrderID = %s""", (order_id,))
        product_id = cursor.fetchone()[0]
        cursor.execute("""INSERT INTO PRODUCTREVIEW (CustomerID, ProductID, Rating, ReviewComment, DateofReview) VALUES(%s, %s, %s, %s, %s)""", (customerID, product_id, Rating, Desc, date.today()))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('thanks.html')

# for showing review of product into the table
@app.route('/productratings', methods = ['POST', 'GET'])
def productratings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT p.ProductID, P.ProductName, AVG(r.Rating) as AverageRating
                        FROM 
                            Product as p
                        Inner JOIN 
                            ProductReview as r
                        Where 
                            p.ProductID = r.ProductID
                        GROUP By 
                            p.ProductID, p.ProductName""")
    allrating = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('allproductrating.html', allrating = allrating)

# for inserting review of product into the table
@app.route('/delivery_review/<int:order_id>', methods = ['POST', 'GET'])
def delivery_review(order_id):
    if(request.method == 'POST'):
        Rating = request.form['Rating']
        Desc = request.form['Desc']
        customerID = session['user_id']
        conn = get_connection()
        cursor = conn.cursor()
        # insert into the rating table
        cursor.execute("""SELECT DeliveryID from MAKEORDER WHERE OrderID = %s""", (order_id,))
        delivery_id = cursor.fetchone()[0]
        cursor.execute("""INSERT INTO AgentReview (CustomerID, DeliveryID, Rating, Content, ReviewDate) VALUES(%s, %s, %s, %s, %s)""", (customerID, delivery_id, Rating, Desc, date.today()))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('thanks.html')


if __name__ == "__main__":
    app.run(debug = True)
    
    
#making of triggers