#rm ~/.local/state/nvim/swap/%home%ankugarg%study%study-notes%postgres%notes.md.swp Postgres Notes
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
```
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

```sql
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
```sql
CREATE ROLE <name_of_user> WITH LOGIN PASSWORD <password>;
```

Example
```sql
CREATE ROLE new_user WITH LOGIN PASSSWORD 'password';
```

#### Granting access to the role
Syntax 
```sql
GRANT CONNECT ON DATABASE <db_name> TO <user_role>;
```

Example
```sql
GRANT CONNECT ON DATABASE postgres TO new_user;
```

This allows user to connect to the database.

#### Revoke access
Syntax
```sql
REVOKE CONNECT ON DATABASE <db_name> FROM PUBLIC;
```

Example
```sql
REVOKE CONNECT ON DATABASE postgres FROM PUBLIC;
```

This prevents all the other users from connecting to the database.

#### Setting up different permissions
```sql
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
```sql
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
```sql
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

### Multiple CTEs in a single query
```sql
WITH plays_cte AS (
  SELECT s.title, s.duration, p.play_duration, p.user_id FROM streaming.plays p
  JOIN streaming.songs s ON p.song_id = s.id 
  WHERE p.play_start_time::DATE BETWEEN '2024-09-15' AND '2024-09-16'
  AND p.play_duration < (s.duration / 2)
),
user_play_counts AS (
  SELECT title, duration, COUNT(DISTINCT user_id) AS user_count, MIN(play_duration) AS min_play_duration,
  COUNT(*) AS total_play_count
  FROM plays_cte
  GROUP BY title, duration 
)
SELECT title, duration, min_play_duration, total_play_count FROM user_play_counts
WHERE user_count >= 3 
ORDER BY min_play_duration ASC 
LIMIT 3;
```


**Note : Postgres doesn't always execute the query which has been defined and will always convert the query into an optimised query.**
If the CTE is called more than once in the query then Postgres will materialise it automatically

## Recursive queries
Recursive queries are the CTE that is created by adding recursive clause to the CTE.
```sql
WITH RECURSIVE cte_name
  (column1, column2, columnN)  # The recursive CTE definition 
AS (
  SELECT columns FROM table1   # The non-recursive part
  WHERE condition
  
  UNION [ALL]

  SELECT columns FROM cte_name # Recursive tem 
  WHERE recursive_condition
)
SELECT columns FROM cte_name;
```


-> The RECURSIVE clause instructs Postgres that the CTE is a recursive query. The definition can include an optional list of columns that are expected to be returned.
-> The non-recursive term is executed once, poulating a temporary working table with the initial data.
-> The UNION or UNION ALL clause merges the results of the non-recursive abd recursive terms until the recursion stops.

A good example explaining the use case is below.
Assume we have a table which contains the songs played by a user on a streaming platform. if a song is played after another song without interruption then it stores the played_after

Now let's say we want to get the list of the songs played by users in a sequence started by a certain song

```sql
WITH RECURSIVE play_sequence AS (
  SELECT id, user_id, song_id,
    play_start_time, play_duration, played_after
  FROM streaming.plays
  WHERE id = 5 

  UNION ALL
  
  SELECT p.id, p.user_id, p.song_id, 
    p.play_start_time, p.play_duration, p.played_after
    FROM streaming.plays p 
    JOIN play_sequence ps ON p.play_after = ps.id
)
SELECT user_id, song_id, play_start_time,
  play_duration as duration, played_after
FROM play_sequence
ORDER BY play_start_time;
```

This query selects the song by id and then builds songs played in which the played_after is set as song id of the original song returned then we join the results

### Arguments in Recursion
Recursive queries allow us to define a list of columns that are carried through recursion.

```sql
WITH RECURSIVE play_sequence(parent_id, sequence, total_duration) AS (
  SELECT id, ARRAY[id], play_duration
  FROM streaming.plays 
  WHERE id = 5 
  
  UNION ALL 
  
  SELECT p.id, ps.seequence, || p.id, total_duration + p.play_duration 
  FROM streaming.plays p 
  JOIN play_sequence ps ON p.played_after = ps.parent_id 
)
SELECT p.song_id, p.play_start_time, p.play_duration, 
  ps.sequence, ps.total_duration
FROM play_sequence ps 
JOIN streaming.plays p ON ps.parent_id = p.id 
ORDER BY ps.sequence, p.play_start_time;
```


**Note : The `ps.sequence || p.id` just appends the id of the new song play to the existing array.**

## Window functions
Window functions allow us to perform calculations on specific columns and arguments. this can be an aggregatee function such as SUM() or AVG()
Syntax
```sql
SELECT function_name(argumrnts)
OVER (PARTITION BY columnA)
FROM table;
```

Suppose we need to calculate the total played duration of a song then we can use below
```sql
SELECT song_id, SUM(play_duration) AS total_duration 
FROM steaming.plays
GROUP BY using song_id ORDER BY total_duration DESC;
```

this is fine but now if we want to show the total_duration for each user who actually played the song
```sql
SELECT song_id, user_id, SUM(play_duration) as total_duration
FROM streaming.plays
GROUP BY (song_id, user_id) ORDER BY song_id;
```


This has a problem because now we are showing the number of plays by each user for a song, this problem can be solved without window function. 
```sql
SELECT DISTINCT p.song_id, p.user_id, t.total_duration
FROM streaming.plays p 
JOIN(
  SELECT song_id,
    SUM(play_duration) AS total_duration
  FROM streaming.plays 
  GROUP BY song_id 
) t ON p.song_id = t.song_id 
ORDER BY p.song_id;
```

The problem with this is that the query is not optimised.

```sql
WITH plays_with_total AS (
  SELECT
    song_id, user_id, SUM(play_duration)
    OVER (PARTITION BY song_id) AS total_duration 
  FROM streaming.plays 
)
SELECT DISTINCT song_id, user_id, total_duration 
FROM plays_with_total 
ORDER BY song_id, user_id;
```


# Indexes
Indexes are the first thing that we turn to when a query is too slow and optimization is required.
If we run a SELECT statement which will try to find a row by the value of the column, then the database needs to iterate through all the rows available in the table. This is a linear search and the time complexity is O(n). As the number of records increase, the query gets slower and slower.
If the column we are looking for is indexed then the search becomes easier. By default the index is a B-tree.

## Types of Indexes
There are 2 broad categories of the index types:
-> By index scope : Here we decide which column of the table needs to be applied to the indexed data. Examples include single-column, composite, covering, partial and functional
-> By data structure : B-tree, hash, bloom, GGIN, RUM, GiST, SP-GiST, BRIN, HNSW

By default the index used is B-Tree 
Syntax
```sql
CREATE INDEX new_index_name ON table_name(colun_name);
```

With data structure
```sql
CREATE INDEX new_index_name ON tableA USING GIN (columnA);
```

Different data structures are suitable for different type of the data stored inside the column.

### Using explain statement
If a query is slow then an explain statement should be used first before deciding which column should be indexed.
Syntax
```sql
EXPLAIN 
SELECT username, level, score 
FROM game.player_stats 
WHERE player_id = 250;
```


Explain statement doesn't actually run the query, for that we need to analyse the statement
```sql
EXPLAIN ANALYZE 
SELECT username, level, score 
FROM game,player_stats 
WHERE player_id = 250;
```


It explains the plan of execution for the query.

### Single-column Indexes
In this type of index, the index is applied to single column only 
#### Single-column B-tree indexes 
B-tree structure allows searching with a time complexity of logrithmic scale. If the number of queries are 1000 then it will only take 3 lookups give then branching factor is 10.
The default index created is B-Tree.
Syntax
```sql
CREATE INDEX idx_score
ON game.player_stats(score DESC);
```

**Note : It is a good practice to run the ANALYZE command after creating an index:**
```sql
CREATE INDEX on tableA(columnB);
ANALYZE tableA;
```

#### Single-column hash indexes 
In this type of index, the value is converted into a hash and the hash is computed and matched with the value directly.
A limitation with hash is that it is useful only for the exact matches.
```sql
CREATE INDEX idx_champion_title
ON game.player_stats
USING hash(champion_title);
```



### Composite column indexes 
Composite column indexes are created over multiple columns in the table. They are also referred as multi column index. 
B-tree, GIN, GiST, BRIN are the different type of indexes supported by Postgres.

**When to use composite indexes?**
This approach is useful when query needs to be executed with multiple column filters. Postgres doesn't always use indexes if it thinks that the approach will be more optimal without the index.
**One would argue why it cannot work with adding a single column index for multiple columns. It is actually not right because of how it will work internally in postgres. For example if we have 2 columns score and region and we index both of them, when a composite query is executed the postgres will first filter the data based on one column and then later based on another column so eventually this doesn't fix the core issue.**

Syntax
```sql
CREATE INDEX idx_region_score_win_count
ON gamee.player_stats (region, score DESC, win_count DESC);
```

Here an index is created in combination of 3 columns. `region`, `score` in descending order, `win_count` in descending order

#### Caveats of using composite indexes 
The index above is optimised for the query where we sort by the score first and then by win_count, however this may not be the case 100% of the times.
If I execute a query which sorts by win_count first then the index can no longer be used.

**Note : After Postgres 18, the support to skip a column was introduced in composite indexes.**

### Covering indexes 
Covering index is an index that stores additional columns from the table, enabling the database to retrieve column values directly without accessing the table rows.
```sql
CREATE INDEX index_name ON table_name(columnA)
INCLUDE(columnB, columnC [, additional_columns]);
```

If a query is present to access the selects the columnB and sorts it by columnC then database doesn't need to access table_name to retrieve the values of columnB and columnC. The values can be directly obtained from index.

### Partial Indexes:
A partial index is an index which is applied to certain part of the data and it can be updated with below syntax
```sql
CREATE INDEX partial_index_name ON table_name(columnA) WHERE condition;
```

### Functional and expression indexes: 
Functional index is also called as expression index, it is useful when the data is stored in different format and the query will always use it in a different format.
```sql
CREATE INDEX idx_perf_margin
ON game.player_stats((win_count - loss_count));
```

>Beware of over-indexing. Indexes are good for improving the performance but this doesn't come for free. Each time an index is created, the postgres maintains it on every writee to the column which has it's own cost.



# Postgres and JSON
Initial support for JSON was introduced in 2012. There are 2 data types which are present.
i) JSON : JSON needs to be used if the database needs to perform certain validation and checks in any field of the JSON, like data type for each field present in the JSON object. 
ii) JSONB : If the object needs to be queried as well then the JSONB can be used.

The use of JSON should be considered when 
i) data is static or updated infrequently (e.g. configurations, metadata)
ii) data is sparse which is characterized by a significant presence of zeros, nulls etc.
iii) Schema flexibility is required or normalization is hard to achieve

Sometimes it doesn't make sense to use normalized table approach because of below reasons :
Write overhead : This would require updating multiple tables transactionally. Say we are storing data related to pizza then we will need to store data in different tables. If a customer orders a pizza with 2 types of veggies then the application will need to insert the data into multiple tables (each table representing different type of topping)

Read Overhead : This would mean that there will be overhead for reading of the data as well.

Transformation : Frontend works with pizza recipes in JSON format - making it easier to display and process orders.


## Advantages of using JSON : 
```sql
SELECT pizza FROM pizzeria.order_items WHERE order_id = 100;
```

This simple query will return all the data we need. 
Sample output 
```bash
pizza
--------------------------------------------------------------------------
{"size": "small", "type": "margherita", "crust": "thin",
"sauce": "marinara", "toppings": {"cheese": [{"mozzarella": "regular"}],
"veggies": [{"tomato": "light"}]}}
{"size": "small", "type": "custom", "crust": "gluten_free",
"sauce": "pesto", "toppings": {"meats": [{"bacon": "light"}],
"cheese": [{"mozzarella": "regular"}], "veggies": [{"onion": "light"}]}}
{"size": "extra_large", "type": "pepperoni", "crust": "thin",
"sauce": "marinara", "toppings": {"meats": [{"salami": "regular"}],
"cheese": [{"mozzarella": "regular"}]}}
(3 rows)
```

In some scenarios, we might need only certain fields and not all of them, also we might need to filter data based on certain field values.
Postgres provides basic operators which provides these capabilities:
1. `->` and `->>` operators : 
These operators extract fields from a JSON object. `->` gives field in JSON format and `->>` converts into text for further processing.
2. `@>` and `?` operators :
`@>` object checks whether a JSON object contains another JSON object and `?` verifies the existence of a specific key in the object.
3. Path expression allows us to check JSON objects for certain valus.

### Extracting fields with the `->` and `->>` operators
```sql
SELECT order_id, ordeR_item_id, pizza->'size' as pizza_size, pizza->>'crust' as pizza_crust FROM pizzeria.order_items WHERE ordeR_id = 100;
 order_id | order_item_id |  pizza_size   | pizza_crust 
----------+---------------+---------------+-------------
      100 |             1 | "small"       | thin
      100 |             2 | "small"       | gluten_free
      100 |             3 | "extra_large" | thin
(3 rows)
```

Here we can note that the `->` operator returns an object and `->>` returns extracted text.
We can use index of a field in JSON array to fetch the details.
```sql
SELECT order_id, order_item_id, pizza->'toppings'->'veggies'->0 as veggies_toppings FROM pizzeria.order_items WHERE ordeR_id = 100;
 order_id | order_item_id |  veggies_toppings   
----------+---------------+---------------------
      100 |             1 | {"tomato": "light"}
      100 |             2 | {"onion": "light"}
      100 |             3 | 
(3 rows)

```


### Using the `?` operator to check for the presence of a key
Example
```sql
SELECT order_id, order_item_id, pizza->'toppings'->'meats' as meats
FROM pizzeria.order_items
WHERE pizza->'toppings' ? 'meats'
ORDER BY order_id LIMIT 5;
```

### Comparing objects with `@>` operator
The containment operator `@>` allows us to check whther one JSON object contains another within its structure.
```
SELECT count(*)
FROM pizzeria.order_items 
WHERE pizza @> '{"crust" : "gluten_free"}';
```

On top of using the containment operator, we can use `->` operator as well.

### Using path expressions
In addition to basic JSON functions and operators, the path expressions are also supported by postgres 
```sql
SELECT order_id, order_item_id, pizza->'toppings'->'meats' AS meats 
FROM pizzeris.order_items 
WHERE jsonb_path_exists(pizza, '$.toppings.meats[*] ? (exists(@.sausage))')
ORDER BY order_id limit 5;
```


Rules :
i) the path expression always starts from $
ii) After $, the expression is followed by field name
iii) [*] gets all the keys present inside the object 
iv) ? equates the condition followed by it 
v) the condition exists(@.sausage) checks if the sausage is present as meat type in any of the toppings 
vi) multiple expressions can be chained together like below 
```sql
SELECT count(*) 
FROM pizzeria.order_items 
WHERE jsonb_path_exists(
  pizza,
  '$ (@.type=="custom") .toppings.cheese[*].parmesan ? (@ == "extra")'
);
```

## Modifying JSON data
Simplest way of updating the data to the database is to first get the data and then update it using the application layer 

Selecting the pizza item 
```sql
SELECT pizza
FROM pizzeria.order_items 
WHERE order_id = $1 AND order_item_id = $2;
```

Updating the pizza item 
```sql
UPDATE pizzeria.order_items
SET pizza = new_pozza_order_json
WHERE order_id = $1 and order_item_id = $2;
```

The simplest way is not the best way, postgres provides a jsonb_set function which allows me to update the JSON objects 
Selecting the existing object 
```sql 
SELECT jsonb_pretty(pizza)
FROM pizzeria.order_items
WHERE order_id = 20 AND order_item_id = 5;
```

Updating the object with new details 
```sql
UPDATE pizzeria.order_items
SET pizza = jsonb_set(pizza,'{crust}','"regular"', false)
WHERE order_id 20 and order_item_id = 5;
```


The function accepts below 
i) The original object 
ii) The path of the target which needs to be updated 
iii) The new value that needs to be updated 
iv) Behavior if the field is missing

## Indexing JSON data
Using an expression with B-Tree index 
```sql 
CREATE INDEX idx_pizza_type 
ON pizzeria.order_items ((pizza ->> 'type'));
```

Using GIN indexes 
In this index, whole JSON object structure is enforced as the index.

# Full text search with Postgres 
## Basics of full-text search in Postgres 
Before the text search below steps are required 
1. Tokenisation : The original text data, usually referred to as a document, is parsed into tokens, which are smaller text components such as words or phrases.
2. Normalization : The database converts the tokens into lexemes which are the basic unit of meaning in a language. Postgres removes case sensitivity, stem tokens to their root forms and removes stop words such as articles and prepositions. 
**Before**
5 explorers are traveling 
**After**
"5","explor","travel"
3. Storing and Indexing : The lexemes are stored in the database to avoid repeating the tokenization and normalization steps. Postgres provides a special data type called tsvector, designed to store lexemes.
4. Searching : The application executes full-text search queries on the lexemes stored in the database.

> The tokens, lexemes can be checked using ts_debug function
```sql
SELECT token, description, lexemes, dictionary
FROM ts_debug('5 explorers are traveling to a distant galaxy');
```

```bash
   token    |   description    |  lexemes  |  dictionary  
------------+------------------+-----------+--------------
 5          | Unsigned integer | {5}       | simple
            | Space symbols    |           | 
 explorers  | Word, all ASCII  | {explor}  | english_stem
            | Space symbols    |           | 
 are        | Word, all ASCII  | {}        | english_stem
            | Space symbols    |           | 
 traveeling | Word, all ASCII  | {traveel} | english_stem
            | Space symbols    |           | 
 to         | Word, all ASCII  | {}        | english_stem
            | Space symbols    |           | 
 a          | Word, all ASCII  | {}        | english_stem
            | Space symbols    |           | 
 distant    | Word, all ASCII  | {distant} | english_stem
            | Space symbols    |           | 
 galaxy     | Word, all ASCII  | {galaxi}  | english_stem
(15 rows)

```
Stemming and stop word removal is done by the parser.

### Full text search configurations 
By default postgres uses certain dictionaries and configurations which are set at time of installation and default language is english.
However these configurations can be updated later.

We can check the list of the configurations present.
```bash
\dF
               List of text search configurations
   Schema   |    Name    |              Description              
------------+------------+---------------------------------------
 pg_catalog | arabic     | configuration for arabic language
 pg_catalog | armenian   | configuration for armenian language
 pg_catalog | basque     | configuration for basque language
 pg_catalog | catalan    | configuration for catalan language
 pg_catalog | danish     | configuration for danish language
 pg_catalog | dutch      | configuration for dutch language
 pg_catalog | english    | configuration for english language
 pg_catalog | finnish    | configuration for finnish language
 pg_catalog | french     | configuration for french language
 pg_catalog | german     | configuration for german language
 pg_catalog | greek      | configuration for greek language
 pg_catalog | hindi      | configuration for hindi language
 pg_catalog | hungarian  | configuration for hungarian language
 pg_catalog | indonesian | configuration for indonesian language
 pg_catalog | irish      | configuration for irish language
 pg_catalog | italian    | configuration for italian language
 pg_catalog | lithuanian | configuration for lithuanian language
 pg_catalog | nepali     | configuration for nepali language
 pg_catalog | norwegian  | configuration for norwegian language
 pg_catalog | portuguese | configuration for portuguese language
 pg_catalog | romanian   | configuration for romanian language
 pg_catalog | russian    | configuration for russian language
 pg_catalog | serbian    | configuration for serbian language
 pg_catalog | simple     | simple configuration
 pg_catalog | spanish    | configuration for spanish language
 pg_catalog | swedish    | configuration for swedish language
 pg_catalog | tamil      | configuration for tamil language
 pg_catalog | turkish    | configuration for turkish language
 pg_catalog | yiddish    | configuration for yiddish language
(29 rows)
```


## Preparing data for full text search 
1. Generating lexemes with the to_tsvector function 
`to_tsvector([config regconfig, ] document text) returns tsvector`
The function accepts 2 arguments 
* `regconfig` : We can specify the existing full-text search configuration discussed earlier 
* `document` : This parameter can be any text

```sql
SELECT * FROM to_tsvector(
'The explorers must save the fragile peeace between Earth and the aliens');
                              to_tsvector                               
------------------------------------------------------------------------
 'alien':12 'earth':9 'explor':2 'fragil':6 'must':3 'peeac':7 'save':4
(1 row)
```

In above result we can see that the stop words are removed but the position is maintained.
If the word is repeated multiple times then the position of both the instances is stored together.
```sql
SELECT * FROM to_tsvector(
postgres(# 'Space Explorers' || ' ' || 'The explorers must save the fragile peace between Earth and the aliens.');
                                    to_tsvector                                     
------------------------------------------------------------------------------------
 'alien':14 'earth':11 'explor':2,4 'fragil':8 'must':5 'peac':9 'save':6 'space':1
(1 row)
```


2. Storing the tsvector lexemes in the database 
The vectors can be stored in below manner
* *Generate lexemes on the fly* : In this case we are not actually storing the lexemes but we are generating the lexeme on the fly.
* *Store lexemes in a column* : The application adds a column of the tsvector type to a table and stores the generated lexemes there.
* *Index lexemes directly* : In this case the lexemes are not stored but are indexed directly. But this requires defining the configuration within the index which may not work in few cases.

```sql
ALTER TABLE omdb.movies
ADD COLUMN lexemes tsvector
GENERATED ALWAYS AS (
to_tsvector(
'english', coalesce(name, '') ||
' ' ||
coalesce(description, ''))) STORED
```

Here we are taking name and description column and then changing it to vector and then storing it into a new column lexemes.

## Performing full text search 
Before performing the search, the search keyword needs to be converted into tsvector data type.
We can combine the lexemes with the help of operators like &, | etc.

Using *plainto_tsquery* 
`plainto_tsquery([config regconfig, ] querytext text) returns tsquery`
Function takes the raw text version of a query via the querytext argument and converts it into the tsquery type.

```sql
SELECT plainto_tsquery('a computer animated film');
      plainto_tsquery       
----------------------------
 'comput' & 'anim' & 'film'
```

`@@` operator is used to execute the query against the column
```sql
SELECT id, name
FROM omdb.movies 
WHERE lexemes @@ plainto_tsquery('a computer animated film');
```

The query works as follows 
1. Transforms the user phrase 
2. Performs the full-text search 
3. Returns the result

We can use advanced queries as well using `to_tsquery`
```sql
SELECT id, name
FROM omdb.movies
WHERE lexemes @@ to_tsquery('computer & animated & (lion | clownfish | donkey)');
```

*Note*
We have `<->` operator which allows us to specify the followed by keyword 
e.g.
lion <-> king means lion is followed by king 
we can also search for instance where there is certain distance between the words
e.g.
return <3> king 
Here the king should be 3rd word after the return 


## Ranking search results 
When we search the data based on text embeddings, the postgres returns all the rows with a match but the order of the responses should be ranked based on the relevance.
Postgres provides `ts_rank` function which provides ranking of response based on relevance.

```sql
SELECT id, name, vote_average,
ts_rank(lexemes, to_tsquery('ghosts')) AS search_rank
FROM omdb.movies
WHERE lexemes @@ to_tsquery('ghosts')
ORDER BY search_rank DESC, vote_average DESC NULLS LAST LIMIT 10;
   id   |               name               | vote_average | search_rank 
--------+----------------------------------+--------------+-------------
    251 | Ghost                            | 6.3333301544 | 0.082745634
 210675 | A Most Annoying Ghost            |              | 0.082745634
   1548 | Ghost World                      | 8.1428575516 | 0.075990885
    620 | Ghostbusters                     | 7.0500001907 | 0.075990885
  57784 | ParaNorman                       |            7 | 0.075990885
  12175 | Ghosts of Goldfield              |            6 | 0.075990885
 185828 | Dhamilo Pani                     |              | 0.075990885
 166008 | Ghosts                           |              | 0.075990885
  84904 | A Girl Walks Home Alone at Night |            9 |  0.06079271
  25028 | Miracolo a Milano                |            8 |  0.06079271
(10 rows)
```

Here we have calculated the rank using `ts_rank` function and then ordered based on the rank score.
In this scenario, the weight of the element is not considered (say we want to show the movies with ghost word included in the name first)
The weights can be passed on to certain columns 

We can store the lexemes in the database like below 
```
ALTER TABLE omdb.movies
ADD COLUMN lexemes tsvector
GENERATED ALWAYS AS (
setweight(to_tsvector('english',coalesce(name, '')), 'A') ||
setweight(to_tsvector('english',coalesce(description, '')), 'B')
) STORED;
```

The records will be stored like below, notice A and B after the lexeme  indicating the weight
If the lexeme is present in the title, then it shows A and it shows B otherwise.
```bash
-[ RECORD 1 ]----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
id      | 3
name    | Varjoja paratiisissa
lexemes | 'aki':11B 'backdrop':37B 'capit':42B 'cashier':20B 'director':10B 'drama':35B 'driver':15B 'fall':22B 'film':3B 'finnish':9B,41B 'garbag':13B 'helsinki':27B 'ilona':21B 'kaurismäki':12B,33B 'love':24B 'mani':31B 'nikand':16B 'paratiisissa':2A 'play':43B 'proletarian':6B 'raini':26B,40B 'role':47B 'special':46B 'supermarket':19B 'trilog':7B 'truck':14B 'unemploy':18B 'varjoja':1A

```

Postgres supports four labels—
A, B, C, and D 
A typically assigned to the highest-priority parts of a document and D to the
lowest-priority parts.
Weights are passed as an array in the format 
{D-weight, C-weight, B-weight, A-weight}.
If the weights argument is omitted, the function uses default values: 
{0.1, 0.2, 0.4, 1.0}. 

The closer the weight is to 1, the higher the priority.

## Highlighting search results 
Sometimes we might need functionality to highlight the term which matches the search term. Postgres has inbuilt capabilities to support that feature.
Postgres provide `ts_headline` function which returns fragments from the document which the query terms are highlighted. Additionally, the function supports the optional regconfig parameter for specifying a full-text search configuration and the options parameter to customize the output of the ts_headline function.

```sql
SELECT id, name, description,
ts_headline(description, to_tsquery('pirates')) AS fragments,
ts_rank(lexemes, to_tsquery('pirates')) AS rank
FROM omdb.movies
WHERE lexemes @@ to_tsquery('pirates:B')
ORDER BY rank DESC LIMIT 1;
-[ RECORD 1 ]------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
id          | 58
name        | Pirates of the Caribbean: Dead Man's Chest
description | Captain Jack is back! The bizarre and infamous pirate Captain Jack is in a battle with the ocean itself. Jack knows it won’t be easy and gathers friends to help him on his mission to find the heart of Davy Jones in this second and more slapstick film from the pirate trilogy.
fragments   | <b>pirate</b> Captain Jack is in a battle with the ocean itself. Jack knows it won’t be easy
rank        | 0.6957388

```
Here fragments don't include all the instances of the query word.

`ts_healine` accepts parameters to increase number of fragments, number of words, delimiter etc.

```sql
SELECT id, name, description, ts_headline(description, to_tsquery('pirates'),
'MaxFragments=3, MinWords=5, MaxWords=10,
FragmentDelimiter=<ft_end>') AS fragments,
ts_rank(lexemes, to_tsquery('pirates')) AS rank
FROM omdb.movies
WHERE lexemes @@ to_tsquery('pirates:B')
ORDER BY rank DESC LIMIT 1;
-[ RECORD 1 ]------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
id          | 58
name        | Pirates of the Caribbean: Dead Man's Chest
description | Captain Jack is back! The bizarre and infamous pirate Captain Jack is in a battle with the ocean itself. Jack knows it won’t be easy and gathers friends to help him on his mission to find the heart of Davy Jones in this second and more slapstick film from the pirate trilogy.
fragments   | bizarre and infamous <b>pirate</b> Captain Jack is in a battle<ft_end>slapstick film from the <b>pirate</b> trilogy
rank        | 0.6957388
```



## Indexing Lexemes :
We are storing lexemes but to make the search more efficient, the lexemes should be indexed.
We can use GIN or GiST indexing for lexemes 
```sql
CREATE INDEX idx_movie_lexemes_gin
ON omdb.movies
USING GIN (lexemes);
```

or 

```sql
CREATE INDEX idx_movie_lexemes_gist
ON omdb.movies
USING GIST (lexemes);
```


# Postgres Extensions 
One of the reasons why the DB has gained so much popularity. Postgres provides multiple extensions and we can view the extension using below statement.
```sql
SELECT count(*) FROM pg_available_extensions;
```

The start working with any extension, we require to do below :
a. Install extension on the Postgres database server.
b. Installing / Enabling the extension

## Enabling the extension
Check if the extension has been installed

```sql
SELECT name, default_version, installed_version
FROM pg_available_extensions
WHERE name ='pgcrypto';
   name   | default_version | installed_version 
----------+-----------------+-------------------
 pgcrypto | 1.3             | 
(1 row)
```

Enable the extension

```sql
CREATE EXTENSION pgcrypto;
```

After installing the extension we can see that the extension is showing correctly 
```sql
SELECT name, default_version, installed_version
FROM pg_available_extensions
WHERE name ='pgcrypto';
   name   | default_version | installed_version 
----------+-----------------+-------------------
 pgcrypto | 1.3             | 1.3
(1 row)

```
Using pgcrypto extension to generate hashed passwords
```sql
INSERT INTO accounts (username, password_hash)
VALUES ('ahamilton', crypt('SuperSecret123', gen_salt('bf')));
```

Here the gen_salt function is using the blowfish algorithm to generate the salt. The salt will be different for each password.
Using salt is important because it reduces the blast radius in case the data is leaked.

## Disabling the extension
```sql
DROP EXTENSION pgcrypto;
```

Important Extensions :
pgvector, pg_ai, and pgvectorscale enable Postgres for generative AI and other
AI/ML workloads, effectively turning it into a vector database. We’ll explore
Postgres’s gen AI capabilities in detail in chapter 8.210
Chapter 7 Postgres extensions
¡ TimescaleDB is a well-known extension that makes it easy to store and analyze
large volumes of time-series and event data. We’ll learn to use Postgres for
time-series workloads in chapter 9.
¡ PostGIS transforms Postgres into a database capable of storing, indexing, and
querying geospatial data. We dedicate chapter 10 to PostGIS and its use cases.
¡ pgmq allows Postgres to function as a lightweight message queue, capable of per-
sisting and delivering application-specific messages and events. We’ll explore
message queuing in Postgres in chapter 11.
¡ pg_duckdb enables high-performance analytical workloads for Postgres. It does so
by embedding DuckDB’s columnar-vectorized storage engine.
The second category of extensions that we, as developers, can benefit from is “pro-
gramming and procedural languages.” In chapter 2, we learned how to create stored
procedures using the PL/pgSQL procedural language. However, you don’t need to
be a PL/pgSQL expert to create custom database functions or procedures that run
inside Postgres. In most cases, you’ll likely find an extension that allows you to write
database functions in your preferred programming language. Here are some examples
for major languages:
¡ PLV8 embeds the V8 JavaScript engine into Postgres, allowing us to write
JavaScript-based database logic and call it from SQL. Additionally, we can use PLV8
together with the PgCompute client-side library to execute JavaScript functions
directly on the database from our application logic, bypassing SQL.
¡ PL/Java, PL/Python, and PL/Rust enable us to create database functions, proce-
dures, and triggers using Java, Python, or Rust, respectively.
The third category of extensions falls under “connectors and foreign data wrappers”
because they allow Postgres to connect to external data sources and query remote data
transparently using standard SQL, as if it were stored in regular Postgres tables. With
this type of extension, Postgres can act as a unified data layer, pulling data from various
sources—some of which might not even support SQL natively. Here are a few examples
from this category:
¡ file_fdw is a foreign data wrapper (FDW) that allows querying data from the file
system.
¡ postgres_fdw, mysql_fdw, oracle_fdw, and sqlite_fdw let Postgres connect to
and query other SQL databases, such as a remote Postgres server, MySQL, Ora-
cle, or SQLite.
¡ redis_fdw, parquet_s3_fdw, and kafka_fdw enable Postgres to retrieve data from
non-SQL data sources such as Redis, S3, and Kafka.
The fourth category of extensions, “query and performance optimization,” helps ana-
lyze query execution statistics and improve performance when necessary. Here are a
few extensions in this category:Postgres-compatible solutions
211
¡ pg_stat_statements helps track the planning and execution statistics of all SQL
statements executed by Postgres.
¡ auto_explain automatically logs execution plans for slow queries, making it
easier to diagnose performance problems without manually running EXPLAIN
ANALYZE.
¡ hypopg adds support for hypothetical indexes, allowing us to test different index-
ing strategies without creating real indexes.
The fifth category, “tools and utilities,” includes extensions that simplify common
Postgres tasks, automate operations, and enhance database usability. Here are a few
examples:
¡ pg_cron is a simple cron-based scheduler that runs in Postgres, helping automate
routine tasks associated with the database.
¡ PostgreSQL Anonymizer lets users anonymize or mask personal and sensitive data
using techniques like dynamic masking and pseudonymization.
¡ pgaudit provides detailed session and object-level audit logging through Post-
gres’s standard logging facility.
¡ pg_partman simplifies the creation and management of both time-based and
number-based table partitions.


# Postgres for generative AI 
## Postgres and LLMs 
Different type os tools LLMs can access
Web tools : Access to web 
Matplotlib : If we want the LLM to generate visualizations 
Infrastructure : LLM can connect to cloud to spin up an instance 
Jupyter environment : LLM can write execute and debug the code 
Postgres : LLM can directly interact with the database to assist the user based on the data available in the database

## Postgres and embedding models : 
Embedding models is another kind of model which is used in gen AI other than LLMs.
A vector embedding is a numeric representation of the words, sentences and other data.
Embedding models are trained to capture the meaning of the sentence.
These models are useful for below use cases 
1. Semantic search 
2. Clustering
3. Recommendations
4. RAG 

## Starting Postgres with pgvector
`pgvector` can be installed similar to other extensions and plugins.

Starting pgvector with volume

```bash
docker volume create postgres-pgvector-volume

docker run --name postgres-pgvector \ 
    -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password \ 
    -p 5432:5432 \ 
    -v postgres-pgvector-volume:/var/lib/postgresql/data \ 
    -d pgvector/pgvector:0.8.0-pg17
```


Enabling extension 
```sql
CREATE EXTENSION vector;
```

## Generating Embeddings : 
Below items are required as minimum : 
1. Target data : The text for which we want to generate the data
2. Embedding model : A model that converts text into vector embeddings. The dimensions of the model play an important role. Generally more accuracy is achieved through model with higher dimensions.
3. Chunking : We need to split huge amount of data into a chunk of data which can be easily fed to the model.
4. Vector DB : A database capable of storing the generated embeddings and supporting vector similarity search.

The vector need to be generated using an embedding model which is provided by multiple services like openai.

## Performing vector similarity search
Vector similarity search is also known as nearest neighbor search or semantic search.
The user types a question in natural language and the application generates an embedding for the query. Then the application generates an embedding for the query.

The similarity is found out by calculating the distance between the vector embeddings.
The pgvector allows consine, euclidean and inner product to calculate the distance.
Cosine is the commonly used for Gen AI applications.

## Indexing vector embeddings
The searching through vectors is a complicated operation. So the search efficiency can be improved by indexing the embeddings.
Below are type of indexes supported by postgres 
1. IVFFlat : This approach indexes the data by listing it as a cluster and uses IVFFlat algorithm to compute the centroids by applying the k-means clustering algorithm.
Creating the index
```sql
CREATE INDEX movie_embeddings_ivfflat_idx
ON omdb.movies
USING ivfflat (movie_embedding vector_cosine_ops) WITH (lists = 5);
```
The statement also defines the WITH (lists = 5) clause, which instructs Postgres to
create the index with five lists. The pgvector documentation (https://github.com/
pgvector/pgvector) suggests choosing the number of lists based on the following
rule:
Choose an appropriate number of lists - a good place to start is rows / 1000 for up to
1M rows and sqrt(rows) for over 1M rows.

The IVFFlat index doesn't always return the correct results because the data is searched from the nearest cluster only. But the result might be present in another cluster.
To improve on this postgres provides probes count .
```BEGIN
BEGIN;
SET LOCAL ivfflat.probes = 3;
SELECT…
COMMIT;
```

This allows using multiple clusters.

This approach is good if the data in the database is relatively stable and no new data is supposed to be entered since the centroid are created at the time of creating index and are not updated later.

2. HNSW : 
Hierarchical Navigable Small World Graph creates a multilayer graph with vector embeddings, where each node represents a vector and edges connect similar vectors based on proximity.
The layers at top are sparsely connected but the layers at the bottom are densely connected.
Creating HNSW index 
```sql
CRREATE INDEX movie_mebeddings_hnsw_idx
ON omdb.movies
USING hnsw (movie_embedding vector_cosine_ops)
WITH (m=8, ef_construction = 16);
```

m defines maximum number of connections per node in the graphs. A higher number of connections creates a denser graph. It also increases index build time and memory usage.
ef_construction : controls the size of the candidate list during index construction. This list holds closest candidates of a particular node during graph traversal.

The parameters need to be modified to check the accuracy of the results, one option is to delete old index and create a new index.
Another option to optimise is to tweak ef_search as below
```sql
BEGIN;
SET LOCAL hnsw.ef_search = 50;
SELECT id, name
FROM omdb.movies
ORDER BY movie_embedding <=>
(SELECT phrase_embedding
FROM omdb.phrases_dictionary
WHERE phrase =
'A movie about a Jedi who fights against the dark side of the force')
LIMIT 3;
COMMIT;
```


When to use what?
1. IVFFlat : when the build time is important and the data would not change significantly.
2. HNSW : When search accuracy is more important 


## Implementing RAG 
Using postgres as a vector database allows us to build sophisticated gen AI applications that combine embedding models with Postgres to help users find relevant information or analyze private data using natural language.
The RAG consists of below parts 
1. Context Retrieval : User prompt is sent to retrieve relevant information present in the DB
2. LLM Augmentation : Provide the retrieved context to the LLM to augment its knowledge.
3. Response Generation Let the LLM perform a task for the user if neccessary 

A RAG system works as below 
1. Request is sent by the customer 
2. Request is converted into embedding through embedding model 
3. Embedding is provided to vector DB for performing a search which returns the context 
4. The context is sent to the LLM along with the question which understands the request and provides response based on the context provided


# Postgres for time series
Time series data is a type of data which has time at which it was recorded at every data point.
For example 
```sql
CREATE TABLE heart_rate_measurements (
  watch_id INT NOT NULL,
  recorded_at TIMESTAMPTZ NOT NULL,
  heart_rate INT NOT NULL,
  activity TEXT NOT NULL CHECK (
    activity IN ('walking', 'sleeping', 'resting', 'workout')
  )
);
```

Considering if the data stored in the table is recorded after interval of one minute, then there will be 1,440 records for each user.
There can be so many records for each day and this can get out of hand very quickly.

Postgres offers *table partitioning* which allows us to split one large logical table into smaller physical tables called partitions
```sql
CREATE TABLE heart_rate_measurements (
  watch_id INT NOT NULL,
  recorded_at TIMESTAMPTZ NOT NULL,
  heart_rate INT NOT NULL,
  activity TEXT NOT NULL CHECK (
    activity IN ('walking','sleeping','resting','workout')
  )
) PARTITION BY RANGE (recorded_at);
```

Here partition by clause defines that the table is split into partitions based on the values of the recorded_at column.

Now the partitions need to be created at regular intervals like below.
For Jan month 
```sql
CREATE TABLE measurements_jan2025
  PARTITION OF heart_rate_measurements
  FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
```
For Feb Month
```sql
CREATE TABLE measurements_feb2025
  PARTITION OF heart_rate_measurements 
  FOR VALUES FROM('2025-02-01') TO ('2025-03-01');
```

This means that the I need to create new tables every month or maybe few months in advance. But this can be solved with help of few extensions which can schedule the creation of the tables.

The main advantage with partition is that we can query between the different partitioned tables with single query.
```sql
SELECT * FROM heart_rate_measurements
WHERE recorded_at BETWEEN '2025-01-30' AND '2025-02-02';
```

Also we don't need to change the table name while creating a new record in the table.
```sql
INSERT INTO heart_rate_measurements (watch_id, recorded_at, heart_rate, activity)
VALUES (1,'2025-01-02 00:00:30+05:30', 80, 'sleeping');
```


## Exploring timescale hypertables
In plain tables, the partition has to be created manually and this is a hassle. But we can use the hypertables which can automatically create the partitions.
Below is a statement can be used to create hypertables.
```sql 
SELECT create_hypertable(
  relation => 'watch.heart_rate_measurements',
  dimenstion => by_range('recorded_at',interval,'1 month'),
  create_default_indexes => false
);
```

The statement covers below 
i. The relation parameter defines the name of the table we want to turn into a hypertable.
ii. The dimension parameter specifies the partitioning method.
iii. create_default_indexes controls whether deafult indexes should be created for the partitioned tables.

The timescale Db uses term chunk for the partition. so terms partition, chunk and child tables are interchangable.

We can use show_chunks which shows the current list of chunks.
The chunks are automatically created and the select statement is optimised to search from the chunks which qualify the criteria.

**The time scale is useful in implementing data retention policy where the data of the users is deleted automatically within 30 days.**


## Analyzing timescale data 
### Using time_bucket function
`time_bucket` function simplifies the aggregation of time-series data. The data can be simplified into 5 mins, hourly, daily, monthly aggregations.
`time_bucket(bucket_width, ts, [origin, timezone, offset])`

### Usingg time_bucket_gapfill
`time_bucket_gapfill`  : Sometimes the data for certain time period may be missing,`time_bucket` usually ignores the time at which there is no period available. This fuction can be used to fill the data for the missing time.
```sql 
SELECT watch_id, time_bucket_gapfill('1 minute', recorded_at) AS minute,
AVG(heart_rate)::int AS avg_rate
FROM watch.heart_rate_measurements
WHERE watch_id=1 AND recorded_at BETWEEN '2025-03-02 07:25'
AND '2025-03-02 07:36'
GROUP BY watch_id, minute ORDER BY minute;
```

```bash
 watch_id |         minute         | avg_rate 
----------+------------------------+----------
        1 | 2025-03-02 07:25:00+00 |      127
        1 | 2025-03-02 07:26:00+00 |      132
        1 | 2025-03-02 07:27:00+00 |      132
        1 | 2025-03-02 07:28:00+00 |      121
        1 | 2025-03-02 07:29:00+00 |      121
        1 | 2025-03-02 07:30:00+00 |         
        1 | 2025-03-02 07:31:00+00 |         
        1 | 2025-03-02 07:32:00+00 |      122
        1 | 2025-03-02 07:33:00+00 |      136
        1 | 2025-03-02 07:34:00+00 |      132
        1 | 2025-03-02 07:35:00+00 |         
        1 | 2025-03-02 07:36:00+00 |      125
(12 rows)

```

This will populate the dates but the data will be missing.
To solve this we can use `LOCF`

```sql 
SELECT watch_id, time_bucket_gapfill('1 minute', recorded_at) AS minute,
LOCF(AVG(heart_rate)::int) AS avg_rate
FROM watch.heart_rate_measurements
WHERE watch_id=1 AND recorded_at BETWEEN '2025-03-02 07:25'
AND '2025-03-02 07:36'
GROUP BY watch_id, minute ORDER BY minute;
```

```bash 
 watch_id |         minute         | avg_rate 
----------+------------------------+----------
        1 | 2025-03-02 07:25:00+00 |      127
        1 | 2025-03-02 07:26:00+00 |      132
        1 | 2025-03-02 07:27:00+00 |      132
        1 | 2025-03-02 07:28:00+00 |      121
        1 | 2025-03-02 07:29:00+00 |      121
        1 | 2025-03-02 07:30:00+00 |      121
        1 | 2025-03-02 07:31:00+00 |      121
        1 | 2025-03-02 07:32:00+00 |      122
        1 | 2025-03-02 07:33:00+00 |      136
        1 | 2025-03-02 07:34:00+00 |      132
        1 | 2025-03-02 07:35:00+00 |      132
        1 | 2025-03-02 07:36:00+00 |      125
(12 rows)
```

## Using continuous aggregates 
### Creating and using aggregates 
A continuous aggregate is a apecial type of Postgres materialized view that stores its precomputed result in hypertable.
These views can be queries like regular tables and the hypertables ensures that the result is partitioned appropriately.
```js 
CREATE MATERIALIZED VIEW watch.low_heart_rate_count_per_5min
WITH (timescaledb.continuous) AS
SELECT
watch_id,
time_bucket('5 minutes', recorded_at) AS bucket,
MIN(heart_rate) as min_rate,
COUNT(*) FILTER (WHERE heart_rate < 50) AS low_rate_count,
COUNT(*) AS total_measurements
FROM watch.heart_rate_measurements
GROUP BY watch_id, bucket;
```

## Refreshing an aggregation policy 
The TimescaleDB extension allows us to define a policy that automatically refreshes a
continuous aggregate. Let’s use the following query to define a sample policy.
```js 
SELECT add_continuous_aggregate_policy
('watch.low_heart_rate_count_per_5min',
start_offset => INTERVAL '15 minutes',
end_offset => INTERVAL '1 minute',
schedule_interval => INTERVAL '1 minute');
```

## Indexing time-series data
Indexing can be used to optimise the queries using the database's built in indexing capabilities.
i. B-tree index
ii. BRIN indexes


