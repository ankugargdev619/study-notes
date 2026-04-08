# Open questions for Postgres
1. What are exclusion constraints, how it is helpful and how to implement it?
Exclusion constraint is used in case where we need to maintain certain instance of a combination to be unique
For example allowing booking of only within a certain range for a certain room
Making sure that user has only one pending order and all the items are added to the order

2. What is b-tree and gist while adding an exclude clause?


3. Need to fully understand the functions syntax in SQL
It starts with CREATE OR REPLACE FUNCTION which allows to create new function if the function doesn't exist and modify it if it is already present.
the statement is followed by name of the function and arguments it accepts like get_order_status(order_id INT)

This is followed by a return statement 

4. How MERGE statement works?

5. How B-tree is used for index?
