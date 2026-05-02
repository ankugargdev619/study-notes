**Hoisting** : 
A clear mental model for hoisting is not about moving the variable outside or reordering. But it is basically about 

Temporal Dead Zone :
Time between the entering the scope and initialization of the variable. Though TDZ is not about time but execution order.

```js 
let a = 10;

{
  console.log(a);
  let a = 20;
}
```

In this case, an error will appear because the inner scope is referencing to a new location in the memory.


```js 
const a;
```

Above code will throw a `SyntaxError` since the value of `const` cannot be changed and it has to be initialized at the time of declaration.

*Hoisting determines where the binding lives and TDZ determines whether it is usable*


TDZ is helpful in preventing accidental shadowing bugs where we reuse an existing variable.

```js 
var x = 10;

function test() {
  console.log(x);
  if (true) {
    var x = 20;
  }
}

test();
```
This will print undefined because the var is scoped inside the function and not inside the block 

```js 
var x = 5;

function test() {
  console.log(x);
  if(true) {
    let x = 20;
  }
}

test();
```

This will print 5 because the x inside the function is scoped inside if statement block only

```js 
var x = 5;

function test() {
  console.log(x);
  var x = x + 10;
  console.log(x);
}

test();
```


Output : NaN 

```js 
var x = 1;

function test() {
  var x = x;
  console.log(x);
}

test();
```

Output : undefined

