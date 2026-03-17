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
```
\c <name of db>
```
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

# Example
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

# Example
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
