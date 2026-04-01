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
