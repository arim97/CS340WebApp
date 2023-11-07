
------------------------------------------------------------------------------------
------ CREATE  ---------------------------------------------------------------------
------------------------------------------------------------------------------------

------ Manager page --------

-- Add a new customer with the values specified
-- can also used with on homepage
INSERT INTO Customers (name, address, phone, date_of_birth) VALUES (%s, %s, %s, %s);

-- Create a new account
-- Account info will be auto generated
-- Balance default = 0
INSERT INTO Accounts (account_id) VALUES (%s);

-- Create a new card
-- card info will be auto generated 
INSERT INTO Cards (card_id, account_id, security_code, exp_date)
VALUES (%s, %s, %s, %s);

----- Banking Functions -----

-- Transfer between accounts
INSERT INTO Transactions (sender_id, destination_id, amount, date, type, comments)
VALUES (%s, %s, %s, %s, %s, %s);

-- Not relevant to this project but would be a core function in a real implementation
-- Deposit into account (No sender_id)
INSERT INTO Transactions (sender_id, destination_id, amount, date, type, comments)
VALUES (NULL, %s, %s, %s, %s, %s);

-- Withdraw from account (No destination_id)
INSERT INTO Transactions (sender_id, destination_id, amount, date, type, comments)
VALUES (%s, NULL, %s, %s, %s, %s);

----------------------------------------------------------------------------------
------ READ  ---------------------------------------------------------------------
----------------------------------------------------------------------------------

-- Display selected account
SELECT * FROM Accounts
WHERE Accounts.account_id = :aidInput;

-- Display all cards associated with account
SELECT * FROM Cards
WHERE Cards.card_id = :aidInput;

----------------------------------------------------------------------------------
------ UPDATE  -------------------------------------------------------------------
----------------------------------------------------------------------------------

-- Update an account's balance
UPDATE Accounts
SET balance = SUM(Transactions.amount)
FROM Accounts
INNER JOIN Transactions ON Accounts.account_id = Transactions.destination_id AND Accounts.account_id = Transactions.sender_id
WHERE Accounts.account_id = :aidInput;

----------------------------------------------------------------------------------
------ DELETE  -------------------------------------------------------------------
----------------------------------------------------------------------------------

-- Delete a customer
DELETE FROM Customers
WHERE customer_id = :csidInput;

-- Delete an account
DELETE FROM Accounts
WHERE account_id = :aidInput;

-- Delete a transaction
DELETE FROM Transactions
WHERE transaction_id = :tidInput;

-- Delete a card
DELETE FROM Cards
WHERE card_id = :cidInput;