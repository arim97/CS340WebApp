
-- DDL for Project Step 2 Draft
-- By Mohamed Ari and Hoang Tran
-- 10/26/2023


-- Turn off foreign key checks
SET FOREIGN_KEY_CHECKS = 0;
--
-- Table structure for table Customers``
--
-- Holds the information for all of the service's customers
DROP TABLE IF EXISTS `Customers`;

CREATE TABLE `Customers` (
    customer_id int(11) NOT NULL AUTO_INCREMENT UNIQUE,
    name varchar(64) NOT NULL,
    address varchar(255) NOT NULL,
    phone varchar(64) NOT NULL,
    date_of_birth date NOT NULL,
    PRIMARY KEY (customer_id)
);


--
-- Table structure for table accounts``
--
-- Holds the information for all accounts in the service
DROP TABLE IF EXISTS `Accounts`;

CREATE TABLE `Accounts` (
    account_id int(11) NOT NULL UNIQUE,
    balance decimal(10,2) NOT NULL DEFAULT 0,
    PRIMARY KEY (account_id)
);




--
-- Table structure for table transactions``
--
-- Holds the information for all transactions processed by the service
DROP TABLE IF EXISTS `Transactions`;

CREATE TABLE `Transactions` (
	transaction_id int(11) NOT NULL AUTO_INCREMENT UNIQUE,
    destination_id int DEFAULT NULL,
    amount decimal(10,2) NOT NULL,
    date date NOT NULL,
    type varchar(64) NOT NULL,
    comments text DEFAULT NULL,
    sender_id int,
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (sender_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
  
);

--
-- Table structure for table Branches``
--
-- Holds the information for all branches of the bank
DROP TABLE IF EXISTS `Branches`;

CREATE TABLE `Branches` (
    branch_id int(11) NOT NULL AUTO_INCREMENT UNIQUE,
    branch_name varchar(255) NOT NULL,
    address varchar(255) NOT NULL,
    phone varchar(64) NOT NULL,
    manager varchar(64) NOT NULL,
    PRIMARY KEY (branch_id)
  
);


--
-- Table structure for table Cards``
--
-- Holds information for all cards associated with an account
DROP TABLE IF EXISTS `Cards`;

CREATE TABLE `Cards` (
    card_id int(11) NOT NULL PRIMARY KEY,
    account_id int(11) NOT NULL,
    security_code int(3) NOT NULL,
    exp_date date NOT NULL,
    CONSTRAINT ucard UNIQUE(card_id, security_code, exp_date),
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE 
  
);


--
-- Table structure for table In_Account``
--
-- Holds the information for which customers are in an account
DROP TABLE IF EXISTS `In_Account`;

CREATE TABLE `In_Account` (
    customer_id INT,
    account_id INT,
    CONSTRAINT inacc UNIQUE(customer_id, account_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE, 
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
  
);

--
-- Table structure for table goes_to``
--
-- Holds information for which branch serves which customer
DROP TABLE IF EXISTS `Goes_to`;

CREATE TABLE `Goes_to` (
    branch_id INT,
    customer_id INT,
    CONSTRAINT clientat UNIQUE(customer_id, branch_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (branch_id) REFERENCES Branches(branch_id) ON DELETE CASCADE ON UPDATE CASCADE
  
);

-- Turn on foreign key checks
SET FOREIGN_KEY_CHECKS=1;
COMMIT;


-- Inserting into table Customers
INSERT INTO Customers
(
    name,
    address,
    phone,
    date_of_birth
)
VALUES
('Hoang Tran', 'SW 15th Random Ave', '206-567-1234', '2023-10-23'),
('Mohamed Ari', 'NW 20th Random Ave', '206-675-3231', '1997-09-23'),
('Hee Ya', '1000 Westlake Ave E', '512-234-1210', '1972-06-30'),
('See Ya', '1000 Westlake Ave E', '514-198-8752', '2006-08-21');

-- Inserting into table Accounts
INSERT INTO Accounts
(
    account_id,
    balance
)
VALUES
(1234567, 1234),
(4725292, 200),
(4321456, 10425),
(3526145, 150);

-- Inserting into table Transactions
INSERT INTO Transactions
(   
    sender_id,
    destination_id,
    amount,
    date,
    type,
    comments
)
VALUES
(4321456, 3526145, 100, '2023-10-23', 'Transfer', NULL),
(4725292, 4321456, 200, '2022-10-26', 'Transfer', 'By Jackson'),
(3526145, 1234567, 50, '2023-01-12', 'Transfer', 'Domain Costs'),
(1234567, NULL, 20, '2024-10-26', 'Withdraw', NULL),
(NULL, 4725292, 7000, '2021-09-12', 'Deposit', NULL);

-- Inserting into table Branches
INSERT INTO Branches
(   
    branch_name,
    address,
    phone,
    manager
   
)
VALUES
('Money Place', 'SW 129th Random Ave', '206-343-2344', 'Nathan Gummy'),
('Cash Location', '2000 Eastlake Ave E', '231-324-8759', 'Holly Fisher'),
('Currency Area', '238 NW 19th St', '541-324-6748', 'Urick Taylor');

-- Inserting into table Cards
INSERT INTO Cards
(
    card_id,
    account_id,
    security_code,
    exp_date
)
VALUES
(200768236, 1234567, 582, '2027-09-01'),
(200972122, 4725292, 321, '2025-04-01'),
(200435262, 4321456, 432, '2029-10-01'),
(200315642, 3526145, 981, '2026-07-01'),
(200426589, 3526145, 121, '2029-09-01');


-- Inserting data into In_Account
-- Which Customers are in Which Account
INSERT INTO In_Account
(
    customer_id,
    account_id
)
VALUES
(04, 4725292),
(03, 4725292),
(03, 4321456),
(01, 3526145),
(02, 1234567);

-- Inserting data into Goes_to
-- Which Customers use which branch
INSERT INTO Goes_to
(
    customer_id,
    branch_id
)
VALUES
(04, 01),
(03, 01),
(01, 01),
(02, 03);





