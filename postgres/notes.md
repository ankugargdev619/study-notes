# Commands to interact with Postgres
## Starting Postgres with docker
```
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
```
docker exec -it <container_name(we used postgres)> psql -U <username (we used postgres)>
```
OR
### Running on a remote server
```
psql -h <instance_url> -U <username> -d <db_name>
```
