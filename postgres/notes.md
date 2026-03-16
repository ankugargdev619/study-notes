## Commands to interact with Postgres
1. Starting Postgres with docker
```
docker volume create postgres-volume
docker run --name postgres \ 
-e POSTGRES_USER=postgres \ 
-e POSTGRES_PASSWORD=password \ 
-p 5432:5432 \ 
-v postgres-volume:/var/lib/postgresql/data \ 
-d postgres:17.2
```

```
```
```
```
```
