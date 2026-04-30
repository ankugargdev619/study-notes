# Closure : 
Closure is not a feature but it's an effect of how Javascript handles the scopes and functions.
**Every function remembers the environment where it was created and not where it was defined.**

When code runs, JS creates an Execution Context which has below
i) Variable Environment 
ii) Lexical Environment 
iii) this binding

Each function has a hidden property [[Environment]] which points to the lexical environment of the function where it was created.

Closure = Function + It's outer reference which contains reference of variable from outer scope 
Important thing to note is that closure doesn't copy the variable but it keeps a reference of the variable.
So if any changes are made in the variable then function has access to the latest value.

Let's understand this with help of an example
```js
function createFunctions() {
  var arr = [];

  for (var i = 0; i < 3; i++) {
    arr.push(function () {
      console.log(i);
    });
  }

  return arr;
}

const fns = createFunctions();
fns[0]();
fns[1]();
fns[2]();
```

# Global Execution Context (Creation Phase)
Memory is allocated for createFunctions and function reference is stored to the memory 
Memory is allocated to fns and the value is uninitialized

# Global Execution Phase
createFunctions() is executed and a new execution context is created.

# createFunctions - Creation Phase
arr is initialized to undefined
i is initialized to undefined 

# createFunction - Execution Phase
arr is assign with []
since i is a var it lives in the function scope and not per iteration 
During first iteration (i=0) a new function is created and a hidden reference of the var i is passed to the function.
During iteration 2 (i=1), another function is created with a hidden reference of the var i 
During iteration 3 (i=2), another function is created with a hidden reference of var i 
During iteration 4 (i=3), loop ends 

Notice at this time the value of i is set to 3.

# Back to Global Execution Phase
`fns[0]()` is called which has reference to value of i through hidden environment. thus logging the value 3.
Similarly `fns[1]()` and `fns[2]()` is executed to log 3.


*Closure is the capability of the functions to be able to use the variables from the scopes in which they were created irrespective of where they are called.*

When a function is finished executing then it is usually destroyed after the Execution context of the function is removed from the call stack but if a function has hidden [[Environment]] reference to any of the variables then the data is not destroyed.

**Scope**
This is a region of the code in which the function is accessible.

```js 
let a = 10;

function test() {
  let b = 20;
  console.log(a); // a is accessible here 
}

console.log(b); // This throws an error 
```

In this case the `a` is accessible everywhere, however `b` is accessible only inside the code block enclosed inside the function.

Types of scopes : 
1. Global Scope : This is for variables which are accessible everywhere.
```js 
let x = 1;
```
2. Function Scope : This is for variables which are available inside a function only
```js 
function fn() {
  let y = 2;
}
```
3. Block Scope : variables enclosed inside a block which can be accessed only inside a code block.
```js
if (true) {
  let z = 3;
}
```

**Note** : Scope is static which means it is used based on where it was created irrespective of where it was called.

## Scope Chain or Lexical scope Chain : 
Whenever a variable is required during execution, js engine first looks for the variable in current scope, then in the outer scope and outer outer scope until it either reaches global scope or the variable is found.

Closure keeps the memory alive even if the variable is not used. It is not garbage collected because closure still references the environment.


