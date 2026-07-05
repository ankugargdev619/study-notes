# FastAPI
It is a high-performance web framework for building APIs with python.
FastAPI is built on top of Starlette and Pydantic

## Starlette : The API receives an http request from client, processes it and provides a response. Starlette is the component which performs all this function.
## Pydantic : It is a data validation library, it is used to validate the input data type, parameters etc.

## Objective of creating FastAPI : 
1. Improve performance of the APIs
2. Improved code writing speed by removing lot of boilerplate

### How the requests are fast?
There are below components of an API service.
a. Web server
b. API code 

Problem with this is that the API code cannot directly understand the info from an http request. So a translator is required in between, the main purpose of this is to translate the http request into a format which python can understand, This is called as SGI - Server Gateway Interface

How is it different from the Flask?
Flask uses WSGI - Werkzeug library is used and Gunicorn is used as server : The biggest disadvantage is that it is synchronous and it is slow because of it's nature
FastAPI uses ASGI - Starlette is used to create SGI and uvicorn is used as server : It is asynchronous in nature and therefore faster.

async - await helps in parallel processing of the requests which means that the requests which take longer are processed in async way allowing to process parallel requests.

### How it is fast to code?
a. Automatic input validation
b. Auto generated interactive documentation and can be accessed by going to /docs 
c. Seamless integration with modern ecosystem


