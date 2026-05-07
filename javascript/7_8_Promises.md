Why promises exist
Javascript is single threaded and it can execute only one thing at a time, if there is any task which takes time to execute then whole system freezes and cannot be used for anything else. Javascript can start async work (timers, HTTP requests, DB calls, file reads)

Before promises, callbacks were used
```js 
getUser(id, (user) => {
  getPosts(user,(posts) => {
    getComments(posts, (comments) => {
      //callback hell 
    })
  })
})
```

The code above was how the async tasks were executed when async calls were dependant on each other.
This had below problems
1. Nested code (hard to read and manage)
2. Difficult error handling 
3. Inversion of control 
4. Difficult composition 

Promise : 
Promise is an object which represents an eventual completion of the task or rejection of the task.
Promise has 3 states
Pending
Fulfilled
Rejected


Internally promise is like below 
When it is not resolved or rejected 
```js 
{
  state : "pending",
  value : undefined,
  handlers : []
}
```

When resolved 
```js 
{
  state : "fulfilled",
  value : 10
}
```

When rejected 
```js 
{
  state : "rejected",
  value : Error()
}
```

Creating promises : 
Creating promise and assigning to a variable:
```js
const promiseOne = new Promise(function (resolve,reject) {
  // Doing an Async task 
  // DB calls, reports generations, network calls etc.
  setTimeout(function () {
    console.log('Async task is complete');
    resolve();
  },1000)
});

promiseOne.then(function () {
  console.log("Promised consumed")
})
```

Chaining promise directly :
```js 
new Promise (function(resolve,reject){
  setTimeout(function() {
    console.log('Async task executed');
    resolve();
  },1000);
}).then(function (){
  console.log("Promise resolved");
}
```

Passing value during resolving:
```JS
const promiseThree = new Promise (function (resolve, reject){
  setTimeout(()=>{
    resolve({name : "Ankit"})
  },1000)
});

promiseThree.then(function (value) {
  console.log(value);
}
);
```

Passing value during rejecting
```js
const promiseFour = new Promise(function(resolve, reject){
  setTimeout(function(){
    let error = true;
    if(!error) {
      resolve({name : "Ankit"});
    } else {
      reject("Error : Something went wrong");
    }
  })
})

promiseFour
.then((user) => {
    console.log(user);
    return user.name
  }).then((username) => {
    console.log(username);
  }).error((error) => {
    console.log(error);
  }).finally(() => {
    console.log("Finally executed");
  });
```


An important caveat with Promises is that the promise constructor is executed synchronously
```js
new Promise((resolve) => {
  console.log("this weill be executed synchronously");
  resolve(); // this is when the callback is pushed into the microtask queue
})

console.log("Outside");
```

Consume using async await

```js
const promiseFive = new Promise(function (resolve, reject) {
  setTimeout(()=> {
    let error = true;
    if(!error) {
      resolve({username : "javascript",password : "password"});
    } esle {
      reject("Error")
    }
  },1000)
})

async function consumePromise (){
  try {
    const response = await promiseFive;
    console.log(response);
  } catch(err) {
    console.log(err);
  }
};

consumePromise();
```


Async await : Async - await is used to handle the promises.
An async function always returns a promise, even when we variable returning a non promise from inside the function.
```js 
async function fn() {
  return "Hello";
}

const data = fn();
console.log(data);
```

Promise execution flow
```js 
console.log("Start");

const p = new Promise((resolve) => {
  console.log("executor");
  resolve(100);
})

p.then(console.log);

console.log("End")
```


The output flow will be as below
Start 
executor
End
100

Important difference between async await and then
```js 
const p = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve("Promise resolved");
  },1000);
})
```

// Using .then()
```js
function getDataThen() {
  p.then(console.log);
  console.log("The internal execution")
}

getDataThen();
```

Output of this will be below
The internal execution 
Promise resolved 


// Using async-await
```js 
async function getDataAsync() {
  const res = await p;
  console.log(res);
  console.log("After the promise");
}

getDataAsync();
```

Output of this will be below 
Promise resolved
After the promise 


The code inside a Promise is executed first but the when resolve is invoked, the callback is added to the microtask queue.

**Note** : .then() always returns a Promise, if the return value is not a promise then it is automatically wrapped inside a promise, this enables then chaining.

Whenever an error is throw, the promise looks for next error handler, if no error is present then an unhandled error is shown

.finally() runs regard less of the success or failure.

Sequential vs Parallel await
Sequential
```js 
const a = await fetchA();
const b = await fetchB();
```

Total time : A + B 

Parallel
```js
const ap = await fetchA();
const bp = await fetchB();

const a  = await ap;
const b = await bp;
```

Total time : max(A,B)


Below id an example of sequential execution
```js 
function delay(ms, value) {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve(value);
    }, ms);
  });
}

async function fetchA() {
  console.log(`[${Date.now()}] fetchA started`);

  const result = await delay(2000, "A");

  console.log(`[${Date.now()}] fetchA finished`);

  return result;
}

async function fetchB() {
  console.log(`[${Date.now()}] fetchB started`);

  const result = await delay(1000, "B");

  console.log(`[${Date.now()}] fetchB finished`);

  return result;
}


async function sequential() {
  console.log("Sequential started");

  const start = Date.now();

  const a = await fetchA();
  const b = await fetchB();

  console.log("Results:", a, b);

  console.log(
    `Sequential total time: ${Date.now() - start}ms`
  );
}

sequential();

```


Output 
Sequential started
[1778137071525] fetchA started
[1778137073527] fetchA finished
[1778137073527] fetchB started
[1778137074528] fetchB finished
Results: A B
Sequential total time: 3003ms


Parallel
```js 
function delay(ms, value) {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve(value);
    }, ms);
  });
}

async function fetchA() {
  console.log(`[${Date.now()}] fetchA started`);

  const result = await delay(2000, "A");

  console.log(`[${Date.now()}] fetchA finished`);

  return result;
}

async function fetchB() {
  console.log(`[${Date.now()}] fetchB started`);

  const result = await delay(1000, "B");

  console.log(`[${Date.now()}] fetchB finished`);

  return result;
}



async function parallel() {
  console.log("Parallel started");
  
  const start = Date.now();

  const pa = fetchA();
  const pb = fetchB();
  
  const a = await pa;
  const b = await pb;

  console.log("Results:", a, b);

  console.log(
    `Sequential total time: ${Date.now() - start}ms`
  );
}


parallel();
```

Parallel started
[1778137246634] fetchA started
[1778137246634] fetchB started
[1778137247635] fetchB finished
[1778137248635] fetchA finished
Results: A B
Sequential total time: 2001ms

Promise combinators:
`Promise.all()` : This fails fast and whole promise is rejected if any one promise is rejected
`Promise.allSettled()` : this never fails and the error for the failed statuses is shown
`Promise.race()` : First settled promise wins either resolved or rejected. This is useful in implementing request timeouts, say a request might keep running forever but we can add a timeout using the Promise.race()
`Promise.any()` : First fulfilled promise wins and rejects if all reject. The rejection will happen only when all the requests fail but even if one promise succeeds then the promise is settled.


