-- We have classified query based on use cases on the tables.


-- 1. Show average Rating of All product selled

--------------------------------------------------------------------------------------------------------------
SELECT ProductName, AVG(rating)
FROM product
JOIN MakeOrder ON Product.ProductID = MakeOrder.ProductID
JOIN ProductReview ON MakeOrder.productID = ProductReview.productID
GROUP BY ProductName;
--------------------------------------------------------------------------------------------------------------


-- 2. Showing Product History of Customer

--------------------------------------------------------------------------------------------------------------
SELECT
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
    Product ON MakeOrder.ProductID = Product.ProductID and MakeOrder.OrderStatus = 'Done'
WHERE 
    MakeOrder.CustomerID = 11
ORDER BY 
    Makeorder.OrderDate;
--------------------------------------------------------------------------------------------------------------


-- 3. Total Sales for the Given Day
--------------------------------------------------------------------------------------------------------------
SELECT SUM(sub.total_price) AS total_sum
FROM (
    SELECT p.Price * m.Quantity AS total_price
    FROM Product p
    INNER JOIN MakeOrder m ON p.ProductID = m.ProductID and m.OrderDate = '2024-03-01'
) AS sub;
--------------------------------------------------------------------------------------------------------------



-- 4. Reduce Quantity of Product when Product is Added into cart for the Given Customer

--------------------------------------------------------------------------------------------------------------
UPDATE product p INNER JOIN cart c ON p.productID = c.productID
SET p.quantity = p.quantity - c.quantity
WHERE c.customerID = 50;
--------------------------------------------------------------------------------------------------------------



-- 5.Total Price of the cart Items of the given Customer

--------------------------------------------------------------------------------------------------------------
SELECT SUM(TotalPrice) AS TotalOrderPrice
FROM Cart
WHERE CustomerID = 11;
--------------------------------------------------------------------------------------------------------------


-- 6. This is for order's by GOLD member's

--------------------------------------------------------------------------------------------------------------
Select 
    mo.OrderID,
    mo.OrderDate
FROM 
    MakeOrder mo
JOIN 
    Customer c ON mo.CustomerID = c.CustomerID
WHERE 
    c.MembershipStatus = 'Gold'
    AND mo.OrderStatus = 'Done';

--------------------------------------------------------------------------------------------------------------



-- 7. Select Top 3 Customer Based on Purchase Amount

--------------------------------------------------------------------------------------------------------------
SELECT 
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
    mo.OrderStatus = 'Done'
GROUP BY 
    mo.CustomerID,
    c.FirstName,
    c.LastName
ORDER BY 
    TotalPurchaseAmount DESC
LIMIT 3;
--------------------------------------------------------------------------------------------------------------



-- 8. Product for a certain order having rating above and equal to 3

--------------------------------------------------------------------------------------------------------------
SELECT 
    p.ProductID, p.OrderID, r.Rating 
FROM 
    MakeOrder p 
INNER JOIN 
    ProductReview r 
ON 
    p.ProductID = r.productID and r.Rating >= 3;
--------------------------------------------------------------------------------------------------------------



-- 9. Arranging all product of Some Specific category in descending order of rating, using like operator for searching a specific category.

--------------------------------------------------------------------------------------------------------------
SELECT 
   ProductName, rating
FROM 
   product
JOIN 
   Category ON Category.CategoryID = Product.CategoryID
JOIN
   ProductReview ON product.productID = ProductReview.productID
WHERE 
   ProductName LIKE 'Spices%' 
Order By 
   rating DESC;
-------------------------------------------------------------------------------------------------------------



-- 10. Total profit per day(for the App store, This happens as from supplier we get product at less rate and sells them at higher rate)
--------------------------------------------------------------------------------------------------------------

SELECT 
    SUM((p.Price - s.PricePerProduct) * m.Quantity) AS TotalProfit
FROM 
    MakeOrder m
INNER JOIN 
    Product p ON m.ProductID = p.ProductID
INNER JOIN 
    Sells s ON p.SupplierID = s.SupplierID AND p.ProductID = s.ProductID
WHERE 
    m.OrderDate = '2024-03-01'; 

--------------------------------------------------------------------------------------------------------------
-- 11. Query to show all undelivered orders for a given customer.

SELECT
    mo.OrderID,
    mo.OrderDate AS OrderPlacedDate
FROM
    MakeOrder mo
WHERE
    mo.OrderStatus = 'Done' AND mo.DeliveryDate IS NULL
    AND mo.CustomerID = 18;
--------------------------------------------------------------------------------------------------------------

-- 12. changing balance of Customer when Item is oredered(assuming customer has enough balance to buy certain product)

UPDATE Customer c 
SET c.Balance = c.Balance - (
    SELECT (m.Quantity * p.Price) from Product p INNER join MakeOrder m ON m.ProductID = p.ProductID and c.CustomerID = m.CustomerID
) Where c.CustomerID > 0; -- this Where clause can be removed
--------------------------------------------------------------------------------------------------------------

-- 13. This query adds more quantity of products for an existing product.

UPDATE Product SET Quantity = Quantity + 100 WHERE productID = 1;

--------------------------------------------------------------------------------------------------------------

-- 14. This query deletes a product from a customer’s cart.

DELETE FROM cart WHERE customerID = 99 AND productID = 14;

--------------------------------------------------------------------------------------------------------------

-- 15. Add New Supplier.

INSERT INTO Supplier (SupplierID, SupplierName, Address, State_Pincode, Hash_Password)
VALUES ([supplier_id], '[supplier_name]', '[address]', 'DL 23838', '[hashed_password]');

--------------------------------------------------------------------------------------------------------------

-- 16. Search for Suppliers in a Specific State.

SELECT * FROM Supplier WHERE State_Pincode LIKE 'DL%'; -- Example: for Delhi

--------------------------------------------------------------------------------------------------------------
-- 17. Count the Number of Suppliers.

SELECT COUNT(*) AS SupplierCount FROM Supplier;

--------------------------------------------------------------------------------------------------------------
-- 18. Appoint Other Admins: Insert a new system administrator into the SystemAdmin table
INSERT INTO SystemAdmin (AdminId, FirstName, LastName, Hash_Password)
VALUES (9, 'New', 'Admin', '[hashed_password]');

