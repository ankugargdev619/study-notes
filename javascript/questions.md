1. **Walk me through, step by step, what happens in memory and on the call stack** when this code runs:

```js
console.log(a);
var a = 10;
function test() {
  console.log(b);
  let b = 20;
}
test();
```

Explain both outputs and why they occur.

2. **What is the exact difference between the Creation Phase and Execution Phase** of an execution context?
   What goes into memory in each phase for `var`, `let`, `const`, function declarations, and function expressions?

3. **Why does `let`/`const` exist in the Temporal Dead Zone before initialization, but `var` does not?**
   Explain this in terms of execution context behavior, not just syntax.

4. **How does the JavaScript engine resolve a variable lookup inside nested functions?**
   Explain scope chain creation and how closure works when the outer execution context has already finished.

5. **What happens to the call stack when a function recursively calls itself 10,000 times?**
   Why does stack overflow happen, and what limits it?

6. **Explain why function declarations are hoisted differently from function expressions.**
   What exactly is stored in memory during creation phase for each of these?

```js
foo();
function foo() {}
bar();
var bar = function() {};
```

7. **When a closure is created, what exactly is being retained?**
   Is the entire outer execution context kept alive, or only certain bindings? Explain precisely.

8. **How does `this` get decided at runtime, and how is that different from lexical scope?**
   Give an example where scope and `this` point to different things.

9. **What is the relationship between execution context and the event loop?**
   If the call stack is busy, what happens to microtasks and macrotasks?

10. **Suppose a function is passed as a callback and executed later.**
    How do its lexical environment, execution context, and `this` behave when it finally runs?

11. **Can two different calls to the same function have two separate execution contexts at the same time?**
    Explain with an example using recursion or async callbacks.

12. **Why does code sometimes behave differently inside `eval()` or `with()`?**
    What do these do to scope resolution and why are they considered dangerous?

Reply with your answers one by one, and I will challenge or refine each answer like a senior interviewer.
