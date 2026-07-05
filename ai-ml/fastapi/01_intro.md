## Introduction
### API
#### What is an API?
APIs are a mechanism that enable two software components such as the frontend and backend of an application.

#### What problem does API solve?
Let's understand this with help of an example. Let's just say that we have irctc website with frontend and backend.
The backend communicates with database and the frontend. The frontend can communicate with the backend without any API using tightly coupled frontend and backend. This is commonly known as monolithic architecture.

The major problem with this is that the application is tightly coupled and if someone wants to use the access of the data.
Say on irctc the websites like mmp, yatra and ixigo need access of the train's data from irctc.
There are below options
1. Shared DB access : No chance
2. Share the backend : The system is tightly coupled and it is kind of impossible to share this data 

Here is where the API comes into play. The backend is decoupled from the frontend. The backend is publicly visible now.
The backend can be accessed directly and available on internet.


This architecture is helpful with having different apps on different OS, websites etc.

API - ML  Perspective : 
Most important think in ML perspective is the ML model.


