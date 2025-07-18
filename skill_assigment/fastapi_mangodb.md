# Fast API  - Async, Sync - Mongo, Console App - CRUD
---
## Overviwe
In this guide, you will learn about FastAPI  nad MongoDb. This article combines conceptual explanations, code examples, and practical insights focused on Python web API development using MongoDB Cloud. 

This guide follows a progressive flow:

- Understanding the basics of MongoDb and FastAPI
- Sync vs Async explained with real examples
- Data validation using Pydantic (FastAPI)
- Preapring of console app using CRUD
- Requirments to run Fastapi application
Interview preparation with Knowledge Check section
By the end, you will have a hands-on understanding of when and how to use Flask or FastAPI effectively.

## Fastapi:- 
### Introduction:-
FastAPI is a modern web framework for building APIs with Python. It is known for being fast, easy to use, and reliable. Built on top of Starlette and Pydantic, it uses Python type hints to provide automatic validation, interactive API documentation, and high performance.
### Key Points:

- Built-in async support
- Auto-generates OpenAPI docs
- High-performance for concurrent workloads

### Install FastAPI:-
The first step is to install FastAPI. Make sure you create a virtual environment(conda environment:- pyhton 3.13 ), activate it, and then install FastAPI by using **pip install fastapi**

### The simplest FastAPI file could look like this:-
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```
To run this app we wnat to install the **uvicorn** by using **pip install uvicorn**. uvicorn is web server to run the fastapi applicatios.

### Interactive API docs
This interactive API docs are use to check the application in wed browser
- Open your browser at http://127.0.0.1:8000
    here we can see the output as a json file
    ```
    {"message": "Hello World"}
    ```
- Now go to http://127.0.0.1:8000/docs.
    You will see the automatic interactive API documentation (provided by Swagger UI).
- And now, go to http://127.0.0.1:8000/redoc.
    You will see the alternative automatic documentation (provided by ReDoc).
### Operation that provided by fastapi
When building APIs, you normally use these specific HTTP methods to perform a specific action.

Normally you use:

1. POST: to create data.(in application we use like **@app.post**)
2. GET: to read data.(in application we use like **@app.get**)
3. PUT: to update data.(in application we use like **@app.update**)
4. DELETE: to delete data.(in application we use like **@app.delete**)

So, in OpenAPI, each of the HTTP methods is called an "operation".

We are going to call them "CRUD operations" too.
### Request Body:-
When you need to send data from a client (let's say, a browser) to your API, you send it as a request body. A request body is data sent by the client to your API. A response body is the data your API sends to the client. Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time, sometimes they only request a path, maybe with some query parameters, but don't send a body. To declare a request body, you use Pydantic models with all their power and benefits.

### Pydantic Models:-
Pydantic is a Python library used for data parsing, validation, and settings management using Python type annotations. It's a key component of FastAPI and is designed to ensure your data is valid, clean, and well-structured.

#### installation of pydentic:- 
**pip install pydantic**

#### Example using pydentic basemodal
```from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    return {"item": item}

```
### Sync vs Async Explained:-
#### Synchronous (Flask):
Blocking request handling
Simpler but inefficient under heavy concurrent requests
#### Asynchronous (FastAPI):
Non-blocking request handling using async/await
Efficient with high concurrency (e.g., database calls, external APIs)
Async Advantage Example:
```
@app.get("/async-task")
async def async_task():
    await some_async_operation()
    return {"status": "done"}
```
### MongoDb:-
