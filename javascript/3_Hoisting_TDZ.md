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

