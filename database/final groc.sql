-- Create Database
CREATE DATABASE Groc;
USE Groc;

-- Customers Table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Contact VARCHAR(15),
    Address TEXT
);

-- Employees Table
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Position VARCHAR(50),
    Salary DECIMAL(10,2)
);

-- Sellers Table
CREATE TABLE Sellers (
    SellerID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Contact VARCHAR(15),
    Address TEXT
);

-- Suppliers Table
CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Contact VARCHAR(15),
    Address TEXT
);

-- Inventory Table
CREATE TABLE Inventory (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    ProductName VARCHAR(100) NOT NULL,
    SupplierID INT,
    Quantity INT DEFAULT 0,
    Price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);

-- Orders Table
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT,
    OrderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(10,2) DEFAULT 0,
    Status ENUM('Pending', 'Completed', 'Cancelled') DEFAULT 'Pending',
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Order Details Table
CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    ProductID INT,
    Quantity INT NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Inventory(ProductID)
);

-- Sales Table
CREATE TABLE Sales (
    SaleID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    SaleDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Total DECIMAL(10,2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

-- Sales Details Table
CREATE TABLE SalesDetails (
    SaleDetailID INT PRIMARY KEY AUTO_INCREMENT,
    SaleID INT,
    ProductID INT,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,
    TotalPrice DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (SaleID) REFERENCES Sales(SaleID),
    FOREIGN KEY (ProductID) REFERENCES Inventory(ProductID)
);

-- Payments Table
CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    PaymentDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    AmountPaid DECIMAL(10,2),
    PaymentMethod ENUM('Cash', 'Credit Card', 'Debit Card', 'UPI', 'Other') NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

-- Returns Table
CREATE TABLE Returns (
    ReturnID INT PRIMARY KEY AUTO_INCREMENT,
    SaleID INT,
    ProductID INT,
    Quantity INT NOT NULL,
    ReturnDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Reason TEXT,
    FOREIGN KEY (SaleID) REFERENCES Sales(SaleID),
    FOREIGN KEY (ProductID) REFERENCES Inventory(ProductID)
);

-- Discounts Table
CREATE TABLE Discounts (
    DiscountID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID INT,
    DiscountPercent DECIMAL(5,2) NOT NULL,
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (ProductID) REFERENCES Inventory(ProductID)
);

-- TRIGGER: Reduce Inventory After Sale
DELIMITER //
CREATE TRIGGER Reduce_Inventory_After_Sale
AFTER INSERT ON SalesDetails
FOR EACH ROW
BEGIN
    UPDATE Inventory
    SET Quantity = GREATEST(Quantity - NEW.Quantity, 0)
    WHERE ProductID = NEW.ProductID;
END;
//
DELIMITER ;

-- PROCEDURE: ProcessSale
DELIMITER //
CREATE PROCEDURE ProcessSale(
    IN p_CustomerID INT,
    IN p_ProductID INT,
    IN p_Quantity INT,
    IN p_PaymentMethod ENUM('Cash', 'Credit Card', 'Debit Card', 'UPI', 'Other')
)
BEGIN
    DECLARE v_AvailableStock INT;
    DECLARE v_UnitPrice DECIMAL(10,2);
    DECLARE v_TotalPrice DECIMAL(10,2);
    DECLARE v_SaleID INT;
    DECLARE v_OrderID INT;

    -- Check stock availability
    SELECT Quantity, Price INTO v_AvailableStock, v_UnitPrice 
    FROM Inventory 
    WHERE ProductID = p_ProductID;

    IF v_AvailableStock < p_Quantity THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient stock!';
    ELSE
        -- Calculate total price
        SET v_TotalPrice = v_UnitPrice * p_Quantity;

        -- Insert a new order for the customer
        INSERT INTO Orders (CustomerID, OrderDate, TotalAmount, Status) 
        VALUES (p_CustomerID, NOW(), v_TotalPrice, 'Completed');

        SET v_OrderID = LAST_INSERT_ID();

        -- Insert sale record
        INSERT INTO Sales (OrderID, SaleDate, Total) 
        VALUES (v_OrderID, NOW(), v_TotalPrice);

        SET v_SaleID = LAST_INSERT_ID();

        -- Insert sale details
        INSERT INTO SalesDetails (SaleID, ProductID, Quantity, UnitPrice, TotalPrice)
        VALUES (v_SaleID, p_ProductID, p_Quantity, v_UnitPrice, v_TotalPrice);

        -- Insert payment record
        INSERT INTO Payments (OrderID, PaymentDate, AmountPaid, PaymentMethod)
        VALUES (v_OrderID, NOW(), v_TotalPrice, p_PaymentMethod);

        -- Update inventory
        UPDATE Inventory 
        SET Quantity = Quantity - p_Quantity 
        WHERE ProductID = p_ProductID;
    END IF;
END;
//
DELIMITER ;


SELECT * FROM INVENTORY;

show COLUMNS FROM inventory