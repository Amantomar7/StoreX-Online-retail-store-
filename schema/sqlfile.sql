

-- This is with data but not data about in some tables

DROP DATABASE IF EXISTS schema_1;
CREATE DATABASE schema_1;
USE schema_1;

CREATE TABLE Customer (
  CustomerID int PRIMARY KEY AUTO_INCREMENT,
  FirstName varchar(255) NOT NULL,
  LastName varchar(255),
  Email varchar(255) NOT NULL,
  Phone varchar(20) NOT NULL,
  Age int NOT NULL,
  Hash_Password varchar(255) NOT NULL,
  MembershipStatus varchar(50) DEFAULT "Bronze" NOT NULL,
  Balance decimal(10,2) DEFAULT 0.00 NOT NULL, 
  Address varchar(255) NOT NULL,
  State_Pincode varchar(10) NOT NULL
);

CREATE TABLE DeliveryAgent (
  DeliveryID int PRIMARY KEY AUTO_INCREMENT,
  FirstName varchar(255) NOT NULL, 
  LastName varchar(255) NOT NULL, 
  Email varchar(30) NOT NULL,
  Phone varchar(20) NOT NULL,
  Address varchar(255) NOT NULL,
  State_Pincode varchar(10) NOT NULL,
  Availability int Default 0, 
  Hash_Password varchar(255) NOT NULL
);

CREATE TABLE Supplier (
  SupplierID int PRIMARY KEY AUTO_INCREMENT,
  SupplierName varchar(255) NOT NULL,
  Address varchar(255) NOT NULL,
  Phone varchar(20) NOT NULL,
  Email varchar(30) NOT NULL,
  State_Pincode varchar(10) NOT NULL,
  Hash_Password varchar(255) NOT NULL
);

CREATE TABLE Category (
  CategoryID int PRIMARY KEY auto_increment,
  CategoryName varchar(255) NOT NULL
);

CREATE TABLE Product (
  ProductID int PRIMARY KEY auto_increment,
  ProductName varchar(255) NOT NULL,
  Price decimal(10,2) NOT NULL,
  CategoryID int NOT NULL,
  ProductDescription text NOT NULL,
  Quantity int NOT NULL,
  SupplierID int NOT NULL,
  FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID),
  FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);

CREATE TABLE Cart (
  CartID int PRIMARY KEY AUTO_INCREMENT,
  CustomerID int NOT NULL,
  ProductID int NOT NULL,
  Quantity int NOT NULL,
  TotalPrice decimal(10,2) DEFAULT 0,
  FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
  FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE Sells (
    SupplierID int, 
    ProductID int, 
    Quantity int NOT NULL,
    PricePerProduct Decimal(10, 2) NOT NULL,
	FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID),
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    PRIMARY KEY (SupplierID, ProductID)
);

CREATE TABLE MakeOrder (
  OrderID int PRIMARY KEY AUTO_INCREMENT,
  CustomerID int NOT NULL,
  DeliveryID int NOT NULL, 
  ProductID int NOT NULL,
  Quantity int Not NULL, 
  OrderStatus varchar(50) NOT NULL,
  OrderDate Date NOT NULL, 
  DeliveryDate Date,
  FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
  FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
  FOREIGN KEY (DeliveryID) REFERENCES DeliveryAgent(DeliveryID)
);

CREATE TABLE ProductReview (
  ReviewID int PRIMARY KEY AUTO_INCREMENT,
  CustomerID int NOT NULL,
  ProductID int NOT NULL,
  Rating int,
  ReviewComment text,
  DateOfReview date NOT NULL,
  FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
  FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);


CREATE TABLE AgentReview (
  ReviewID int PRIMARY KEY AUTO_INCREMENT,
  CustomerID int NOT NULL,
  DeliveryID int NOT NULL,
  Rating int,
  Content text,
  ReviewDate date NOT NULL,
  FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
  FOREIGN KEY (DeliveryID) REFERENCES DeliveryAgent(DeliveryID)  
);

CREATE TABLE SystemAdmin (
  AdminID int PRIMARY KEY AUTO_INCREMENT,
  FirstName varchar(255) NOT NULL,
  LastName varchar(255) NOT NULL,
  Email varchar(20) NOT NULL,
  Phone varchar(20) NOT NULL,
  Hash_Password varchar(255) NOT NULL
);

INSERT INTO Customer (FirstName, LastName, Email, Phone, Age, Hash_Password, MembershipStatus, Balance, Address, State_Pincode) 
VALUES
('Raj', 'Patel', 'raj.patel@example.com', '9876543210', 28, 'hashedpassword11', 'Gold', 1500.00, '12 MG Road', 'MH 400001'),
('Priya', 'Sharma', 'priya.sharma@example.com', '9876543211', 25, 'hashedpassword12', 'Silver', 1200.00, '45 Gandhi Nagar', 'DL 110001'),
('Amit', 'Kumar', 'amit.kumar@example.com', '9876543212', 35, 'hashedpassword13', 'Bronze', 800.00, '78 Nehru Street', 'TN 600001'),
('Neha', 'Das', 'neha.das@example.com', '9876543213', 30, 'hashedpassword14', 'Gold', 2000.00, '90 Sardar Lane', 'GJ 380001'),
('Sanjay', 'Gupta', 'sanjay.gupta@example.com', '9876543214', 45, 'hashedpassword15', 'Silver', 1800.00, '123 Gandhi Road', 'KA 560001'),
('Anjali', 'Mukherjee', 'anjali.mukherjee@example.com', '9876543215', 32, 'hashedpassword16', 'Bronze', 1000.00, '56 Tagore Nagar', 'WB 700001'),
('Rahul', 'Banerjee', 'rahul.banerjee@example.com', '9876543216', 27, 'hashedpassword17', 'Gold', 2200.00, '34 Vivekananda Marg', 'UP 226001'),
('Sneha', 'Reddy', 'sneha.reddy@example.com', '9876543217', 40, 'hashedpassword18', 'Silver', 1900.00, '67 Krishna Street', 'AP 500001'),
('Ravi', 'Choudhary', 'ravi.choudhary@example.com', '9876543218', 33, 'hashedpassword19', 'Bronze', 1100.00, '89 Patel Nagar', 'RJ 302001'),
('Meera', 'Joshi', 'meera.joshi@example.com', '9876543219', 29, 'hashedpassword20', 'Gold', 2500.00, '101 Malviya Avenue', 'MP 462001');

-- Categories
INSERT INTO Category (CategoryName) 
VALUES
('Traditional Clothing'),
('Spices & Condiments'),
('Tea & Coffee'),
('Musical Instruments'),
('Yoga & Meditation'),
('Dance & Music'),
('Health & Wellness'),
('Cookware'),
('Instruments');

-- Supplier
INSERT INTO Supplier (SupplierName, Address, State_Pincode, Hash_Password, Email, Phone)
VALUES
('Silk Emporium', '25 Market Street', 'MH 400001', 'supplierhashedpassword11', "supplier1@email.com", "9989979996"),
('Ethnic Fashion House', '78 Fashion Avenue', 'DL 110001', 'supplierhashedpassword12', "supplier2@email.com", "9989979991"),
('Spice Traders Pvt. Ltd.', '10 Spice Market', 'TN 600001', 'supplierhashedpassword13', "supplier3@email.com", "9989979992"),
('Tea Gardens Pvt. Ltd.', '45 Tea Estate', 'GJ 380001', 'supplierhashedpassword14', "supplier4@email.com", "9989979993"),
('Music Masters', '30 Instrument Road', 'KA 560001', 'supplierhashedpassword15', "supplier5@email.com", "9989979994"),
('Yoga Essentials Pvt. Ltd.', '15 Asana Street', 'WB 700001', 'supplierhashedpassword16', "supplier6@email.com", "9989979995"),
('Nritya Dance Productions', '20 Nritya Lane', 'UP 226001', 'supplierhashedpassword17', "supplier7@email.com", "9989979997"),
('AyurHerbs', '5 Ayurveda Lane', 'AP 500001', 'supplierhashedpassword18', "supplier8@email.com", "9989979910"),
('Tandoor Works', '8 Clay Oven Street', 'RJ 302001', 'supplierhashedpassword19', "supplier9@email.com", "9989979911"),
('Sitar Creations', '12 Musician Avenue', 'MP 462001', 'supplierhashedpassword20', "supplier10@email.com", "9989979912");

-- Products
INSERT INTO Product (ProductName, Price, CategoryID, ProductDescription, Quantity, SupplierID)
VALUES
('Saree', 999.99, 2, 'Traditional Indian attire for women', 50, 2),
('Kurta', 699.99, 2, 'Traditional Indian attire for men', 100, 3),
('Spices Box', 149.99, 3, 'Assorted Indian spices for cooking', 75, 4),
('Tea Set', 499.99, 4, 'Traditional Indian tea set with kettle and cups', 30, 5),
('Tabla', 399.99, 5, 'Classical Indian percussion instrument', 80, 6),
('Yoga Mat', 299.99, 6, 'High-quality yoga mat for practicing yoga', 40, 7),
('Kathak Dance DVD', 1499.99, 7, 'Instructional DVD for learning Kathak dance', 20, 8),
('Ayurvedic Supplements', 399.99, 8, 'Natural health supplements based on Ayurveda', 50, 9),
('Tandoor Oven', 129.99, 9, 'Traditional clay oven for making Indian bread and kebabs', 60, 10),
('Sitar', 79.99, 10, 'Indian classical string instrument', 90, 11);

-- DeliveryAgent
INSERT INTO DeliveryAgent (FirstName, LastName, Phone, Hash_Password, Email, Address, State_Pincode)
VALUES
('Rakesh', 'Singh', '9876543200', 'deliveryhashedpassword11', "deliveryagent1@email.com", '25 Market Street', 'MH 400001'),
('Suresh', 'Yadav', '9876543201', 'deliveryhashedpassword12', "deliveryagent2@email.com", '25 Market Street', 'MH 400001'),
('Deepak', 'Sharma', '9876543202', 'deliveryhashedpassword13', "deliveryagent3@email.com", '25 Market Street', 'MH 400001'),
('Rajesh', 'Patil', '9876543203', 'deliveryhashedpassword14', "deliveryagent4@email.com", '25 Market Street', 'MH 400001'),
('Sandeep', 'Kumar', '9876543204', 'deliveryhashedpassword15', "deliveryagent5@email.com", '25 Market Street', 'MH 400001'),
('Vikram', 'Choudhary', '9876543205', 'deliveryhashedpassword16', "deliveryagent6@email.com", '25 Market Street', 'MH 400001'),
('Ganesh', 'Reddy', '9876543206', 'deliveryhashedpassword17', "deliveryagent7@email.com", '25 Market Street', 'MH 400001'),
('Prakash', 'Joshi', '9876543207', 'deliveryhashedpassword18', "deliveryagent8@email.com", '25 Market Street', 'MH 400001'),
('Harish', 'Khan', '9876543208', 'deliveryhashedpassword19', "deliveryagent9@email.com", '25 Market Street', 'MH 400001'),
('Manoj', 'Shukla', '9876543209', 'deliveryhashedpassword20', "deliveryagent10@email.com", '25 Market Street', 'MH 400001');

-- Admin 
INSERT INTO SystemAdmin (FirstName, LastName, Hash_Password, Email, Phone)
VALUES
('Aditi', 'Sharma', 'adminhashedpassword1', 'admin1@email.com', '9449339221'),
('Vikram', 'Patel', 'adminhashedpassword2', 'admin2@email.com', '9449339222'),
('Neha', 'Rajput', 'adminhashedpassword3', 'admin3@email.com', '9449339223'),
('Rahul', 'Gupta', 'adminhashedpassword4', 'admin4@email.com', '9449339224'),
('Priya', 'Singh', 'adminhashedpassword5', 'admin5@email.com', '9449339225');

Insert into Sells(SupplierID, ProductID, Quantity, PricePerProduct) 
Values 
(1, 1, 100, 20),
(2, 2, 100, 30),
(3, 3, 100, 20),
(4, 4, 1234, 34),
(5, 5, 123, 56.09),
(6, 6, 234, 34.23),
(7, 7, 23, 12.3),
(8, 8, 10, 9.23),
(9, 9, 100, 100.12),
(10, 10, 100, 12.12);