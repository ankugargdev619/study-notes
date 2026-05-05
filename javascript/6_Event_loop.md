Javascript is single threaded but it allows async behavior with help of below architecture.
- Engine
  - Call Stack
  - Memory Heap
- Runtime / Web APIs
  - setTimeout, fecth etc.
- Event Loop
  - Task Queue
  - Micro task queue

## Execution Flow
+--------------------------------------------------+
|               JavaScript Runtime                  |
+--------------------------------------------------+

        +-----------------------------+
        |       Call Stack            |
        |  (Execution Contexts)       |
        +-------------+---------------+
                      |
                      |
                      v
        +-----------------------------+
        |        Web APIs             |
        | (Timers, DOM, Fetch, etc.) |
        +------+----------+-----------+
               |          |
               |          |
               v          v
   +----------------+   +----------------------+
   | Microtask Queue|   |   Callback Queue     |
   | (Promises, etc)|   | (setTimeout, etc.)   |
   +--------+-------+   +----------+-----------+
            |                      |
            |                      |
            +----------+-----------+
                       |
                       v
             +-------------------+
             |    Event Loop     |
             +---------+---------+
                       |
                       |
                       v
                +-------------+
                | Call Stack  |
                +-------------+

1. Call stack executes sync code : pushed to stack -> executed -> popped 
2. Async API is offloaded to Web API and timer starts: `setTimeout(() => console.log("c",0);`
3. Once time finishes, the callbacks are pushed into task or macro task queue and the promises are pushed into microtask queue
4. Event loop : Check if the call stack is empty then priortize microtasks first and then if no micro tasks are present then it executes macro tasks.

## Microtask vs Microtask
Microtasks 
- `Promise.then`
- `queueMicrotask`
- `MutationObserver`

Macrotasks
- `setTimeout`
- `setInterval`
- `setImmediate`
- I/O 

```js 
console.log("start");

setTimeout(() => console.log("timeout"), 0);

Promise.resolve().then(() => console.log("promise"));

console.log("end");
```

Here Promise will be executed first which is a micro task.

## Event Loop cycle
Pseudocode
```js 
while(true) {
  if(callStackEmpty) {
    runAllMicrotasks();
    runAllMacrotaks();
  }
}
```

Edge Cases : 
1. Microtasks keep getting added then the callback in the callback queue will never be executed.
2. setTimeout(0) is not executed immediately, the execution is handed over to Web API, it waits for 0 secs before pushing it into a callback queue. Though it is pushed immediately to the queue, the event loop will wait until the main stack is available i.e. the stack is empty.
3. Callback stack follows FIFO policy 


```
