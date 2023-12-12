
------------------------------------------------------------------------------------
------ CREATE  ---------------------------------------------------------------------
------------------------------------------------------------------------------------
-- Accounts Page
-- Add a new customer with the values specified
-- can also used with on homepage
INSERT INTO Customers (name, address, phone, date_of_birth) VALUES (%s, %s, %s, %s);

-- Create a new account
-- Balance default = 0
INSERT INTO Accounts (account_id) VALUES (%s);

-- Create a new card
-- card info will be auto generated 
INSERT INTO Cards (card_id, account_id, security_code, exp_date)
VALUES (%s, %s, %s, %s);



----------------------------------------------------------------------------------
------ READ  ---------------------------------------------------------------------
----------------------------------------------------------------------------------

-- Display selected account
SELECT account_id as ID, balance FROM Accounts

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

UPDATE Cards SET account_id = %s,security_code = %s, exp_date = %s WHERE card_id = %s;

UPDATE Branches SET branch_name = %s,address = %s, phone = %s, manager = %s WHERE branch_id = %s;

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

DELETE FROM Branches
WHERE branch_id = :cidInput;