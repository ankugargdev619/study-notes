## `this` 
The keyword refers to t he context where a piece of code or function is supposed to run.
When a method is invoked in context of a standalone function, `this` refers to global object. However when `this` is called in context of an object then `this` refers to the object.

In most programming languages, `this` refers to the instance of object in which the method is being called. However in javascript it changes based on how a function is called.
The default behavior can be changed by using `this`, `bind`, `call`, `apply`

When a function is invoked, JS engine creates an Execution Context :
The execution context contains
Variable Environment
Lexical Environment
this binding

The value is this is defined based on how the function is called.
**Note** : It is defined during the creation phase of the FEC.

A function can be called using multiple ways.
1. Global Function : 
```js 
function test() {
  console.log(this);
}
test();
```

In this case the this will refer to the global object which will be `window` for a browser in this case.

2. Method call attached to object
```js 
const obj = {
  firstName : "Ankit",
  lastName : "Sharma",
  greet() { console.log(this.firstName + " " + this.lastName)}
}

obj.greet();
```

In this case the `this` keyword refers to the object itself

3. Constructor
```js 
function Person(firstName, lastName) {
  this.firstName = firstName;
  this.lastName = lastName;

  this.greet = function () {
    console.log(this.firstName + " " + this.lastName);
  };
}

const user1 = new Person("Ankit", "Sharma");

user1.greet(); // Ankit Sharma
```

In this case, the this refers to the new instance of the object, user1 in this case 

## `call()`
Call allows setting up the binding of the `this` keyword immediately at the time of calling.
The syntax is below
```js 
fn.call(thisArg, arg1, arg2)
```

This syntax call the function immediately.

```js 
function greet(city) {
  console.log(`Hi, I am ${this.name} from ${city}`);
}

const user = {name : "Ankit"};

greet.call(user, "Delhi");
```

`call` basically is a method on functions and when a function is invoked through this method, the default binding of the `this` is over-ridden by the this argument object set during the calling.

Edge Cases
1. If null or undefined is passed then the in non-strict mode, the binding points to globalObject else binding points to undefined.
`fn.call(null);`
2. Primitive Value : In this case Js does boxing by setting `ThisBinding = new String("Ankit")`
`foo.call("Ankit");`
3. Arrow functions : The call method is ignored in case of arrow functions, so for arrow functions, it is as good as calling without call method



## `apply()`
Apply is same as call but in this case, the arguments of the function are passed as an array. Apply is used when the number of arguments are dynamic.
Apply behaves same as call but it builds the arguments first and then invokes call internally.
```js 
function foo(a,b) {
  console.log(this.name,a,b);
}

const user = {name : "Ankit"};

foo.apply(user, [10,20]);
```


Edge cases:
1. If null or undefined is passed then the behavior is same as call 
2. Passing non-array arguments : This throws an TypeError
3. Apply can be called using array like data structure instead of array as engine internally converts the object into an array
```js 
const arrLike = { 0: 10, 1: 20, length: 2 };

foo.apply(user, arrLike);
```

## `bind()`
Bind is different from call and apply. It returns a new function with update bindings of `this`.
```js 
function greet() {
  console.log(this.name);
}

const user = { name: "Ankit" };

const boundFn = greet.bind(user);

boundFn(); // "Ankit"
```

Priority rules of binding 
new > bind > call/apply > implicit

```js 
function greet() {
  this.name = "Changed";
}

const obj = { name: "Ankit" };

const bound = greet.bind(obj);

const instance = new bound();

console.log(obj.name);
console.log(instance.name);
```

In this case, the new ignores the binding completely and a new instance is created with no reference of hard binded this.
So this will print "Ankit", "Changed"

```js 
function greet(name) {
  this.name = name;
}

const obj = { name: "Ankit" };

const bound = greet.bind(obj, "Rahul");

const instance = new bound("Priya");
```

This will return Rahul.

When a `new bound("Priya")` is created, this will be interpreted like below

```js 
function bound(...args) {
  return greet.apply(this, ["Rahul", ...args]);
}
```

It is about controlling 2 things, who controls this object and who controls the arguments.
The this is controlled by new and over rides the this 

The greet function is setting the name to the argument it accepts. in this case the arguments are controlled by bound object so Rahul will prrint

**Note** : when a function is bound it cannot be bound again 
