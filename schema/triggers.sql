DROP TRIGGER IF EXISTS ReduceBalance;
DELIMITER $$
CREATE TRIGGER ReduceBalance AFTER INSERT ON MakeOrder
FOR EACH ROW
BEGIN
    UPDATE Customer SET Balance = Balance - (Select price from product where productID = new.productID) WHERE CustomerID = NEW.CustomerID;
END;
$$
DELIMITER ;


DROP TRIGGER IF EXISTS Delivery;
DELIMITER $$
CREATE TRIGGER Delivery AFTER INSERT ON MakeOrder
FOR EACH ROW
BEGIN
    UPDATE DeliveryAgent SET Availability = 1 WHERE DeliveryID = NEW.DeliveryID;
END;
$$
DELIMITER ;



