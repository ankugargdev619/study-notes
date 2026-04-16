# Postgres Notes
# Commands to interact with Postgres
## Starting Postgres with docker
```bash
docker volume create <name of volume (e.g. postgres-volume)>
docker run --name <name of container (e.g. postgres)> \ 
-e POSTGRES_USER=<name of user (e.g. postgres)> \ 
-e POSTGRES_PASSWORD=<password for the user (e.g. postgres)> \ 
-p <PORT_MAPPING (postgres runs with 5432:5432 by default)> \ 
-v <volume data path (e.g. postgres-volume:/var/lib/postgresql/data)> \ 
-d postgres:17.2
```
## Connecting to postgres 
### Running inside docker
```bash
docker exec -it <container_name(we used postgres)> psql -U <username (we used postgres)>
```
OR
### Running on a remote server
```bash
psql -h <instance_url> -U <username> -d <db_name>
```

## Create Tables
```sql
CREATE TABLE <table_name> (
  <col_name> <data_type>,
  <col1_name> <data_type>
);
```
Example
```sql
CREATE TABLE trades (
  id bigint,
  buyer_id integer,
  symbol text,
  order_quantity integer,
  bid_price numeric(5,2),
  order_time timestamp
);
```


## Get list of all the tables
```sql
SELECT datname FROM pg_database;
```

## Change database
```bash
\c <name of db>
```

## List all available schemas
```bash 
/dn   # The default schema is public unless a new schema is defined
```

## Create new schema
```sql
CREATE SCHEMA <schema_name>;
```

## Check the current schema which is selected
```sql
SHOW search_path;
```

## Change schema
```sql
SET search_path TO <schema_name>
```

## create a new | 
```sql
create table <table_schema>.<table_name> (
  <column_name> <data_type>
);

example
create table control_plane.products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT NOT NULL,
  category TEXT CHECK (category IN('coffee','mug','t-shirt')),
  price NUMERIC(10,2),
  stock_quantity INT CHECK (stock_quantity >= 0)
);
```

## List all tables
```bash
\d
```

## Inserting content into a table
```sql
INSERT INTO <schema>.<table>
  (col1, col2, col3)
  VALUES
  ('col1_row1', 'col2_row1', 'col3_row1'),
  ('col1_row2', 'col2_row2', 'col3_row2')
  ('col1_row3', 'col2_row3', 'col3_row3');

# Example
INSERT INTO control_plane.products
  (name, description, category, price, stock_quantity)
  VALUES
  ('Cappacino','Cappacino','coffee',5.00,10);
```

# Query the data
```sql
SELECT <col1>,<col2>..., <coln> FROM <schema>.<table>
WHERE <condition>;
```

Example
```sql
SELECT id, name, price FROM product.catalog
WHERE category='coffee';
```


# Run bash commands
```bash
\! <command>

#Example
\! clear # This clear the console

```

# Update the data in certain row
```sql
UPDATE <schema>.<table> SET <col>=<value>
WHERE <condition>;
```

Example

```sql
UPDATE product.catalog SET price=11
WHERE category='coffee';
```



## Constraints
Multiple constraints can be applied at database level to make sure that the data is valid and there are below common constraints available in postgres
NOT NULL : This ensures that the value on the column cannot be null
UNIQUE : Guarantees that a column or group of columns don't contain duplicate value
PRIMARY KEY : Col or group of cols that may serve as unique identifier
FOREIGN KEY : Value in a column must match row in another table
CHECK : A constraint which allows user to define a custom constraint like a value should be from selected array of values
EXCLUSION : This constraint makes sure that when 2 rows compared on specified column then at least one should return null or false (actual use cases further)

### Check Constraint 
This constraint allows us defining certain rules preventing invalid data entry like negative values etc.
Syntax
```sql
ALTER TABLE <schema>.<table>
  ADD CONSTRAINT <name of constraint> CHECK (<constraint condition>);
```


Example
```sql
ALTER TABLE public.prices
  ADD CONSTRAINT catalog_price_check CHECK(price > 0);
```

### Foreign Key Constraint 
This constraint allows user to store a relation with a column of another table, a condition for setting foreign key constraint is that the column being referred should be unique in the table. This is important because db needs to check if the value is valid for each entry and the process becomes faster if the column is indexed. Since the unique keys are indexed by default, therefore this becomes important.

Syntax
```sql
ALTER TABLE <schema>.<table>
  ADD CONSTRAINT <constraint_name>
  FOREIGN KEY (<local_column_refernce>) REFERENCES <foreign schema>.<table with foreign key>;
```

Example
```sql
ALTER TABLE products.reviews
  ADD CONSTRAINT product_review_product_id_fk
  FOREIGN KEY (product_id) REFERENCES products.catalog(id);
```

### Exclusion Constraint
This is very powerful constraint which allows add constraint in combination of multiple column, it is better understood with help of an example.
Say we want to implement a booking system which books rooms for a hotel. We need to not allow users to book a same room with different dates. This can be a challenging implementation. If I add unique key constraints to the room then I cannot book same room on different dates. If I add unique key constraint to the booking date then it doesn't allow me to book different rooms with same date. This is where the Exclusion constraint is helpful. It is used in combination with GIST and TSRANGE.

Let's first create a schema like below.
```sql
CREATE TABLE reservations
(
 id serial PRIMARY KEY,
 room_id INTEGER,
 booking_status TEXT,
 start_date TIMESTAMP,
 end_date TIMESTAMP,
 EXCLUDE USING GIST (TSRANGE(start_date, end_date) WITH &&)
);
```

What this constraint does is that it doesn't allow adding any entries in the table which lie within start and end date, given an entry is already present.
Though this is still not correct, because this restricts me from booking 2 different rooms with overlapping dates.
The correct solution will be
```sql
CREATE TABLE reservations
(
  id serial PRIMARY KEY,
  room_id INTEGER,
  booking_status TEXT,
  start_date  TIMESTAMP,
  end_date  TIMESTAMP,
  EXCLUDE USING GIST (room_id WITH=, TSRANGE(start_date, end_date) WITH &&)
);
```

Now what is allows is that user can book different rooms with overlapping dates but the same room with overlapping dates cannot be booked.

## Transactions
Whether single or multiple records are required to be updated, all the updated are processed through transactions in Postgres. It follows the basic principles of ACID. The transaction will either be committed or rolled back.
Atomicity : Each transaction is treated as a separate entity and can either be committed or rolled back.
Consistency : Whenever a transaction is executed, the constraints are checked automatically to ensure the data consistency.
Isolation : Ensure that concurrent transactions do not interfere with each other.
Durability : Guarantees that the once transactions is committed, the data is saved permanently even on restart.

The transactions can be of 2 types:
### Implicit
Each query execution is treated as a transaction internally by Postgres. This includes all the INSERT, UPDATE, DELETE etc.
### Explicit
This is invoked when multiple queries are required to be run together. A good way to understand with help of an example is bank transaction.
Transfer $100 from account A to account B, this involves below steps:
a. Reduce the balance from account A by $100
b. Increase the balance of account B by same amount
Multiple things may go wrong with this and we don't want one transaction to complete and other transaction to fail. If we execute the queries inside explicit transaction then both the transactions will be rolled back if any of the query execution fails.

Example
```sql
BEGIN; # Start of the transaction

// Reduce the balance of account A by $100
UPDATE account SET balance = balance - 100 WHERE account_id = 'A';
// Add $100 to the account B
UPDATE account SET balance = balance + 100 WHERE account_id = 'B';

COMMIT; # End of the transaction
```

## Multiversion Concurrence Control (MVCC)
This allows execution of multiple transactions concurrently. Let's understand the problem it solves with help of an example. 

Consider that user A is sending $100 to user B and user B is checking the account balance at same time. Within the transaction assume that the account balance for B has been updated but the transaction is not committed yet. Now at this time if the user B checks the account balance then the account balance will show as original balance + $100 but this is inaccurate since the transaction is not committed yet, this is known as **Dirty Read**. 
MVCC makes sure that data shows only as per transactions which have been completed.

Another scenario can be when 2 different transactions are trying to write the same column. Say user A send $100 to user B and user C sent $50 to user A at same time.
Now the user A's account balance during the transaction will be original balance - 100, but since the transaction is not committed yet, therefore the user C will still see the original balance and if the write is allowed then the user A's balance will become original balance + 50, this is known as **Dirty Reads**.
MVCC prevents this by blocking the second transaction until first transaction is executed.



## Joins
Join queries are used when the data between different table is supposed to be joined together and displayed in a single table.
The syntax is simple with the ON command.

Syntax:
```sql
SELECT <table1_alias>.<col in table> FROM <schema>.<table> <alias>
  JOIN <table>.<col> <ALIAS> ON <alias>.<col> = <alias>.<col>;
```

Example : Say we have 2 tables accounts in customers schema and orders table in sales schema and we want to select the total number of order per customer then we can join the data as below
```sql
SELECT c.name, c.id, count(*) as total_orders
  FROM customers.accounts c 
  JOIN sales.orders s ON c.id = s.customer_id
  GROUP BY c.id 
  ORDER BY total_orders DESC 
  LIMIT 3;
```

What this query does?
It selects the table orders inside sales schema with alias s and table accounts inside customer schema aliased as c.
Join the tables on id column in accounts table is mapped to the customer_id column in the sales schema.

There can be multiple type of joins
### INNER JOIN
This join selects the rows which have values matching in both the tables.
Consider I'm INNER JOINING 2 tables products and categories and we do a join on the id column then the rows with matching id will be selected. The normal join is inner join by default.
Example
```sql
SELECT product_id, product_name, category_name FROM products
  INNER JOIN categories ON products.category_id = categories.id;
```

### LEFT JOIN 
This join selects all the rows from the left table irrespective of whether the value is present in the right table.
Example
```sql
SELECT product_id, product_name, category_name FROM products
  LEFT JOIN categories ON products.category_id = categories.id;
```

### RIGHT JOIN 
This join selects all the rows from right table irrespective of whether it is present in the left table.
Example
```sql
SELECT product_id, product_name, category_name FROM products
  RIGHT JOIN categories ON products.category_id = categories.id;
```

### FULL JOIN 
This join select the rows from both the tables irrespective of the values in other table.
```
SELECT product_id, product_name, category_name FROM products
  FULL JOIN categories ON products.category_id = categories.id;
```

### CROSS JOIN 
This join takes cartesian product of the columns in both the rows. It will show all the possible combinations of both the tables. This is useful in generating all the possible combinations of all the columns. This needs no columns based on which t he values can be matched.
```sql
SELECT product_id, product_name, category_name
FROM products
CROSS JOIN categories;
```


## Functions and Triggers
### Functions
Functions and be simply used make calculations on the fly within the database.
Syntax
```sql
CREATE OR REPLACE FUNCTION products.get_product_price(product_id INT)
RETURNS NUMERIC(10,2) AS $$
  SELECT price
  FROM products.catalog
  WHERE id = product_id;
$$ LANGUAGE sql;
```

This function named get_product_price returns the price of a product given that we pass the product id to it.
Using functions is helpful when we need to implement a business logic at multiple places and it is easier to rather make all the services use a function at database level.

In above example, the function is applied on the products schema and can be called by the application layer easily.
Implementing database functions makes more sense when I need more round trips between DB and application layer if any complex logic needs to be implemented.

**Note**:
Functions vs Stored Procedures
The functions are different from stored procedures. The stored procedures never return a value.

Procedures can be used when batch of data needs to be processed with rollback.

```bash
CREATE OR REPLACE FUNCTION sales.order_add_item(customer_id_param INT, product_id_param INT, quantity_param INT)
RETURNS TABLE (order_id UUID, prod_id INT, quantity INT, prod_price DECIMAL) AS $$
DECLARE pending_order_id UUID;
BEGIN
  SELECT id INTO pending_order_id FROM sales.orders
  WHERE customer_id = customer_id_param
  AND status = 'pending'
  LIMIT 1;

  IF pending_order_id IS NULL THEN
    INSERT INTO sales.orders (customer_id, status)
    VALUES (customer_id_param, 'pending')
    RETURNING id INTO pending_order_id;
  END IF;

  MERGE INTO sales.order_items AS oi 
  USING (
    SELECT id, price FROM products.catalog
    WHERE id = product_id_param
  ) AS prod ON oi.product_id = prod.id AND oi.order_id = pending_order_id
  
  WHEN MATCHED THEN
    UPDATE SET quantity = quantity_param
  WHEN NOT MATCHED THEN
    INSERT (order_id, product_id, quantity, price) VALUES (pending_order_id, prod.id, quantity_param, prod.price);
  RETURN QUERY
  
  SELECT oi.order_id, oi.product_id, oi.quantity, oi.price as prod_price
  FROM sales.order_items as oi
  WHERE oi.order_id = pending_order_id;
END;
$$ LANGUAGE plpgsql;
```

_Understanding the query line by line_ 
Line # 1 : Declared the function with arguments defined in it so the name of the function is order_add_item and arguments are below
a. customer_id_param
b. product_id_param
c. quantity_param
Line # 2 : Defines the return type of the function similar to any function. In this case we are returning the order_id, prod_id, quantity and prod_price and $$ marks the start of code block 
Line # 3, a variable pending_order_id is defined, which will be used in the function
Line # 4 marks the beginning of the function logic 
Line # 5 to 7 we first load the pending order id for the customer, this checks if an order already exists
Line # 9-13 : If the pending order doesn't exist then add a new order and return the value of id into the pending order id 
Line # 15-24 : The merge statement finds the price of the product from the product.catalog table and then updates the sales.order_items table



## Triggers
Triggers are particular type of function which needs to be executed either before or after an update. The triggers are useful for event driven architecture.
A good use case of triggers is to update the billing amount whenever an item is either added or removed from the cart.
When I add any item to a cart then the order amount should get updated and this can be handled using the application layer.
But if we attach a trigger to calculate the amount whenever an item is added or removed from the cart then the logic becomes very consistent.

Syntax
```sql
CREATE TRIGGER trigger_update_order_total
AFTER INSERT OR UPDATE OR DELETE ON sales_order_items 
FOR EACH ROW 
EXECUTE FUNCTION sales.update_order_total();
```

A very good use case is sending notification based on event triggers. This allows using Postgres as messaging queue.

## Views
Views are named queries which return the data in a tabular format. Imagine a query which needs to be executed in multiple places then a view can be used to make it happen.

Syntax
```sql
CREATE VIEW sales.product_sales_summary AS SELECT
c.name AS product_name,
c.category,
SUM(oi.quantity) AS total_quantity_sold,
SUM(oi.quantity * oi.price) AS total_revenue FROM products.catalog c 
LEFT JOIN sales.order_items oi ON c.id = oi.product_id GROUP BY c.id 
ORDER BY total_quantity_sold DESC, total_revenue DESC;
```

By default the views are not materialised which means that the views are not stored, the execution happens at real time. 
If the response of the queries need to be stored and fetched periodically then the materialised views can be used

### Materialized Views
This used for queries which take very long to execute, the queries are executed and response is saved, this response can be served from the storage and the query will not be executed at real time.

Syntax
```sql
CREATE MATERIALIZED VIEW sales.product_sales_summary AS SELECT
date_trunc('month', o.order_date) AS sales_month, SUM(oi.quantity * oi.price) AS total_revenue, COUNT(DISTINCT(o.id)) 
AS total_orders
FROM sales.orders o 
JOIN sales.order_items oi ON o.id = oi.order_id
GROUP BY sales_month
ORDER_BY sales_month;
```

A downside of the materialised views is that the data needs to be refreshed manually by refreshing the view
A period sync of the views can be done using `pg_cron` or this can be attached as a response to a trigger.

### Roles and permissions
It is less than ideal for all the users to have all the permissions to make any changes in the database.
Check the database roles in postgres
`\du`

There should be specific roles for different type of roles. The permissions can be granted like below.

#### Create a role
Syntax 
```bash
CREATE ROLE <name_of_user> WITH LOGIN PASSWORD <password>;
```

Example
```bash
CREATE ROLE new_user WITH LOGIN PASSSWORD 'password';
```

#### Granting access to the role
Syntax 
```bash
GRANT CONNECT ON DATABASE <db_name> TO <user_role>;
```

Example
```bash
GRANT CONNECT ON DATABASE postgres TO new_user;
```

This allows user to connect to the database.

#### Revoke access
Syntax
```bash
REVOKE CONNECT ON DATABASE <db_name> FROM PUBLIC;
```

Example
```bash
REVOKE CONNECT ON DATABASE postgres FROM PUBLIC;
```

This prevents all the other users from connecting to the database.

#### Setting up different permissions
```bash
GRANT USAGE ON SCHEMA public TO <user_name>;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA <schema_name> TO <user_name>;
GRANT USAGEE, SELECT ON ALL SEQUENCE IN SCHEMA products TO coffee_chain_admin;
```

Below are type of grants that can be provided
1. SELECT : Allow SELECT from any column of the specified table, view or sequence.
2. INSERT : Allows INSERT of a new row into the specified table.
3. UPDATE : Allows updating any column of the specified table.
4. DELETE : Allows deleting a row from the specifieid table.
5. RULE : Allows creation of RULE in any table
6. REFERENCES : Allows creating a foreign key constraint 
7. TRIGGER : Allows creation of a trigger on the specified table.
8. CREATE : Allows creation of new databases, create new objects and creation of new tables. 
9. TEMPORARY : Allow temporary tablees to be created while using the specified database.
10. EXECUTE : Allows the use of the specified function and the use of any operators that are implemented on top of the function.
11. USAGE : For procedural languages, allows the use of the specified language.
12. ALL PRIVLEGES : Grant all of the available privleges at once.


# Modern SQL 
Postgres has modern SQL capabilities which allows users to do much more than classic relational capabilities.
Today SQL supports arrays, JSON objects and custom composite unstructured data efficiently.

## Common Table expressions (CTE):
CTEs allows us to break the large queries into small managable queries pieces.
Syntax
```bash
WITH <cte_name> AS (
auxiliary_statement
)
primary_statement
```


The auxiliary statement is a statement which is used at multiple places and can be used in combination with the existing primary_statement.
Using CTEs improves below
i) Improved Readability
ii) Reusability in the same query
iii) Easy debugging
iv) Supprts Recursion
v) Better organization

Example
```bash
WITH plays_cte AS (
  SELECT s.title, s.duration
  FROM streaming.plays p 
  JOIN streaming.songs s ON p.song_id = s.id 
  WHERE p.play_start_time:: DATE BETWEEN '2024-09-15' AND '2024-09-16'
  AND p.play_duration = s.duration 
)
SELECT title, COUNT(*) AS play_count
FROM plays_cte
GROUP BY title
ORDER BY play_count DESC;
```


