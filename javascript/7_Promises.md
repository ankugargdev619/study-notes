Promise : 
Promise is an object which represents an eventual completion of the task or rejection of the task.

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
