# Prototypes and Inheritance
## Core problem Javascript had to solve
```js 
function createUser(name) {
  return {
    name,
    greet: function () {
      console.log("Hello " + this.name);
    }
  };
}

const u1 = createUser("Ankit");
const u2 = createUser("Rahul");
```

Here when createUser is called to initialize the object, the memory is allocated for 2 different objects and the function inside is copied to both the objects creating duplicate even though the function performs same task.

## Fixing the issue manually
```js 
const userMethods = {
  greet: function () {
    console.log("Hello " + this.name);
  }
};

function createUser(name) {
  const user = Object.create(userMethods);
  user.name = name;
  return user;
}

const u1 = createUser("Ankit");
const u2 = createUser("Rahul");
```

Now the object initialize the with a reference to the function which will not be duplicated in the memory.

## Using prototype 
```js 
function User(name) {
  this.name = name;
}

User.prototype.greet = function () {
  console.log("Hello "+this.name);
}

const u1 = new User("Ankit");
```

Here new is actually doing below internally
```js 
const obj = {} // create an empty object 
obj.__proto__ = User.prototype; // Set the prototype of the object to prototype of the User

User.call(obj,"Ankit"); // Call the User function, this initialize the value of name to Ankit 

return obj; // Return the object 
```

Prototypes are used only in the functions because only functions can be used to create objects with shared behavior.

Property Lookup : 
When a property is not found in an object, then the algorithm checks it in prototype which goes up a level and keeps going one level up until either the property is found or prototype is returned null.

## Shadowing
```js 
User.prototype.role = "user";

const u1 = new User("Ankit");
u1.role = "admin";
```

The prototype is only looked if the property is not found in the object itself.
But since in this case, the object already has the value then the value is taken from the object itself.

Therefore it is shadowing the property not overriding it.
```js 
function User(name) {
  this.name = name;
}

function greet(){
  console.log("Hi",this.name);
}

User.prototype.role = "member";

const user = new User("Ankit");
user.role = "admin";

console.log(user.role,Object.getPrototypeOf(user).role);
```

If you check the output of this then you will notice that the property role is still present in the prototype of the object user but since the value is already present in the object itself then the prototype lookup is not required.

## Never override 
```js 
function User(name) {
  this.name = name;
}

function greet(){
  console.log("Hi",this.name);
}

User.prototype.role = "member";
User.prototype.access = "limited";

const user = new User("Ankit");
console.log(user,Object.getPrototypeOf(user));

// Never replace the prototype because the prototype will be replaced for all the objects which have been already created
User.prototype = {
  role : "admin"
};

console.log(user,Object.getPrototypeOf(user));
```

```js 
User.prototype = { role : "admin"}
```
creates a new prototype object but the old objects are still pointing to Prototype at old memory address so they are unable to see this change.

## Classes in Javascript internally use prototype
```js 
class User {
  constructor(name) {
    this.name = name;
  }

  greet() {
    console.log(this.name);
  }
}
```

above class translates to

```js 
function User(name) {
  this.name = name;
}

User.prototype.greet = function () {
  console.log("Hi",this.name);
}
```

1. Never use `__proto__`
This was not part of the original design
It allows runtime mutation of object structure
Security & unpredictable

2. Difference between `prototype`, `__proto__` and `Object.getPrototypeOf`
`prototype` : Exists only on functions which can be used a constructor. It is the object that will become the `[[Prototype]]` of the instance when created using `new`
`__proto__` : This exists on all the object, it is used internally to get and set value of the prototype. Should not be used as per standard practice as using it may break down the optimizations and security vulnerabilities.
`Object.getPrototypeOf` : It is a standard way to read prototype.

