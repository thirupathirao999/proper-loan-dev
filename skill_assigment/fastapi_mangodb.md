# A Complete Learning Guide For Fastapi and MongoDb with Console APP Using CRUD Oparetions
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
---
## Section 1: Fastapi:- 
### Introduction:-
FastAPI is a modern web framework for building APIs with Python. It is known for being fast, easy to use, and reliable. Built on top of Starlette and Pydantic, it uses Python type hints to provide automatic validation, interactive API documentation, and high performance.
### Key Points:

- Built-in async support
- Auto-generates OpenAPI docs
- High-performance for concurrent workloads

### Install FastAPI:-
The first step is to install FastAPI. Make sure you create a virtual environment(conda environment:- pyhton 3.13 ), activate it, and then install FastAPI by using **pip install fastapi**

### The simplest FastAPI file could look like this:-
``` python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```
To run this app we wnat to install the **uvicorn** by using **pip install uvicorn**. uvicorn is web server to run the fastapi applicatios.

### Interactive API docs:-
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
### Operation that provided by fastapi:-
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

### installation of pydentic:- 
```pip install pydantic```

#### Example using pydentic basemodal:-
```python
from fastapi import FastAPI
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

```python
@app.get("/async-task")
async def async_task():
    await some_async_operation()
    return {"status": "done"}
```
## Section 2:  MongoDb:-
### Introduction:-
MongoDB is the most popular NoSQL open source document-oriented database. The term 'NoSQL' means 'non-relational. This means that MongoDB is not based on a table like relational database structure but provides an altogether different mechanism for storage and retrieval of data in json formate.
### A simple MongoDB document Structure:-
``` python
{
  title: 'Mongodb',
  by: 'Harshit Gupta',
  url: 'https://www.mongodb.org',
  type: 'NoSQL'
}
```

### Installing MongoDB:-
Just go to [http://www.mongodb.org/downloads] and select your operating system out of Windows, Linux, Mac OS X and Solaris. A detailed explanation about the installation is provided
### What is a Cluster,database, coolection in MongoDB:-
1. Cluster:- A cluster is a group of MongoDB servers (or instances) that work together to store your data.
2. Database:- A database is a container for collections. It's similar to a schema in SQL.
3. collection:- A collection is a group of documents (records).

#### Example:-
```python
MongoDB Cluster
   └── Database (e.g., "my_app")
         └── Collection (e.g., "users")
               └── Document (e.g., {"name": "Ali", "age": 30})
```

### Methods In Mongodb:-(CRUD operetions):-
| Operation | Command                       |
| --------- | ----------------------------- |
| Create    | `insertOne()`, `insertMany()` |
| Read      | `find()`, `findOne()`         |
| Update    | `updateOne()`, `updateMany()` |
| Delete    | `deleteOne()`, `deleteMany()` |

1. **Insert() :-** The insert() method is a fundamental operation in MongoDB that is used to add new documents to a collection. This method is flexible, allowing developers to insert either a single document or multiple documents in a single operation, which can significantly enhance performance and reduce the number of database calls.
2. **insertOne() :-** It is used to insert a single document in the collection.
3. **insertmany() :-** It is used to insert multiple documents in the collection.
4. **find() :-**	It is used to retrieve documents from the collection.
5. **findOne() :-** Retrieves a single document that matches the query criteria.
6. **updateOne():-** It is used to update a single document in the collection that satisfy the given criteria.
7. **updateMany():-** It is used to update multiple documents in the collection that satisfy the given criteria.
8. **deleteOne():-** It is used to delete a single document from the collection that satisfy the given criteria.
9. **deleteMany():-**	It is used to delete multiple documents from the collection that satisfy the given criteria.

### Integration with Python:-
```pip install pymongo```
### coneting to database:-
```python 
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["users"]

collection.insert_one({"name": "Bob", "age": 28})
```
---
## section 3:- Console APP Using CRUD Oparetions with fastapi and mangodb:-
Refer to the console-based API implemented using the CRUD folder structure


## section 4:- Interview Qutions:-
1. **What is FastAPI, and what are its core advantages over Flask?**

    FastAPI is a modern Python framework used to build APIs quickly using async features.
    Core advantages over Flask:
    - Built-in async support
    - Automatic request validation with Pydantic
    - Auto-generated API docs
    - Faster for high-concurrency applications

2. **What is the role of Starlette and Pydantic in FastAPI?**

    Starlette: Handles web routing, middleware, and async capabilities.

    Pydantic: Handles data validation and serialization using Python type hints.

3. **How does FastAPI automatically generate documentation?**
    FastAPI uses OpenAPI (Swagger) and ReDoc to auto-generate docs based on route definitions and Pydantic models. Visit /docs or /redoc to view them.

4. **Explain the difference between synchronous and asynchronous routes in FastAPI.**

    Synchronous (def): Blocks execution, suitable for simple or CPU-bound tasks.

    Asynchronous (async def): Non-blocking, ideal for I/O operations like DB access.

5. **What is the purpose of uvicorn in FastAPI development?**
    uvicorn is an ASGI server used to run FastAPI applications. It supports async and handles web requests efficiently.

6. **What happens when you visit http://127.0.0.1:8000/docs in a FastAPI app?**
    You get an interactive Swagger UI interface that displays all routes and allows you to test them directly in the browser.

7. **List all the HTTP methods supported by FastAPI for CRUD operations.**

    POST – Create

    GET – Read

    PUT – Update

    DELETE – Delete

8. **Explain what happens if you define a route without the async keyword in FastAPI.**
    The route will still work, but it becomes synchronous (blocking). This may cause performance issues with concurrent requests, especially with slow I/O operations.

9. ****What is MongoDB, and how is it different from relational databases like MySQL?**
    MongoDB is a NoSQL database that stores data in JSON-like documents. Unlike MySQL:

    No fixed schema

    No joins

    Ideal for flexible and nested data

10. **What is a document, collection, and database in MongoDB?**

    Document: A single JSON object (record).

    Collection: A group of documents (like a table).

    Database: A container for collections.
11. **What is the purpose of find() and findOne() in MongoDB?**

    find(): Retrieves all matching documents.

    findOne(): Retrieves the first matching document only.

12. **What is the difference between updateOne() and updateMany()?**

    updateOne(): Updates the first matching document.

    updateMany(): Updates all matching documents.

13. **How does deleteOne() differ from deleteMany() in MongoDB?**

    deleteOne(): Deletes the first document that matches.

    deleteMany(): Deletes all documents that match the condition.

14. **What is a cluster in MongoDB, and why is it important in cloud deployments?**
    A cluster is a group of MongoDB servers that work together for scalability, high availability, and data redundancy. Essential in cloud setups like MongoDB Atlas.

15. **Can MongoDB handle unstructured data? Explain how.**
    Yes. MongoDB can store documents without a fixed schema, allowing different structures in the same collection.

16. **How do you structure a basic FastAPI + MongoDB CRUD application?**

    Use FastAPI for route handling

    Use Pydantic for data validation

    Use PyMongo to interact with MongoDB

    Implement routes for CRUD operations (create, read, update, delete)

17. **What package is used to integrate MongoDB with Python in FastAPI apps?**
    PyMongo – installed via pip install pymongo

18. **What are some challenges in integrating async FastAPI routes with PyMongo (which is synchronous)?**
    PyMongo is synchronous and can block FastAPI’s async event loop. Solution:

    Use a thread executor

    Use an async MongoDB driver like Motor

19. **How do you make your FastAPI app more secure when working with user input and database operations?**

    Validate all inputs with Pydantic

    Use parameterized queries

    Sanitize inputs to prevent injection

    Limit database access

20. **What is the difference between insertOne() and insertMany()?**
    insertOne() inserts one document, insertMany() inserts multiple.