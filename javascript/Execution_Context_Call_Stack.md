## How Javascript executes the code 
All the code inside javascript runs inside an execution context.
When the program is loaded, the `Global Execution Context` is created by the Engine. There can be only 1 global execution context.

**Execution Context**
It is an internal object created by Javascript engine to execute the code. It contains below elements.
i. Lexical Environment : This is an environment where the code runs and it contains below:
a. Environment Record : Stores reference of variables and functions
b. Outer Reference : Link to the parent scope

ii. Variable Environment : A variable environment is a special part of which stores only var variables and function declarations. This environment usually doesn't change much after creation.

+--------------------------------------------------+
|                Execution Context                 |
+--------------------------------------------------+
|                                                  |
|  +--------------------------------------------+  |
|  |            Lexical Environment             |  |
|  |--------------------------------------------|  |
|  |  Environment Record                        |  |
|  |   ├── let, const                           |  |
|  |   ├── function declarations                |  |
|  |                                            |  |
|  |  Outer Reference ----------------------┐   |  |
|  +----------------------------------------|---+  |
|                                           |      |
|  +----------------------------------------v---+  |
|  |            Variable Environment            |  |
|  |--------------------------------------------|  |
|  |  Environment Record                        |  |
|  |   ├── var variables → undefined            |  |
|  |   ├── function declarations                |  |
|  +--------------------------------------------+  |
|                                                  |
|  +--------------------------------------------+  |
|  |            This Binding                    |  |
|  |--------------------------------------------|  |
|  |  this → depends on how function is called  |  |
|  +--------------------------------------------+  |
|                                                  |
+--------------------------------------------------+

Difference between Lexical Environment and Variable Environment
Lexical Environment                Variable Environment
-------------------              -----------------------
Stores:                           Stores:
- let (stored in TDZ)            - var
- const (stored in TDZ)          - function declarations
- block-scoped bindings

Scope type:                      Scope type:
- Block scope                    - Function scope

Updates during execution?        Updates during execution?
- YES (dynamic changes)          - Mostly static after creation

Used in modern JS?               Used in modern JS?
- YES (primary system)           - Legacy behavior (for var)





To keep track of execution context, call stack is used.
Initially Global Execution Context is stored at top of Call Stack.

Each execution context runs in 2 phases
1. Creation Phase : In this phase, a Lexical Environment is created which stores below :  
i. Environment Records : The memory allocated to an object is stored and managed inside the environment record
ii. Outer Environment : This refers to the outer lexical environment which is used to manage the scope, the value is `null` for global execution context. This allows accessing the variable outside the environment using scope chain.

2. Execution Phase
Javascript reads the code line by line and looks for the values inside the lexical environment to show the values.
During execution if a fucntion is called, a new execution context is created for the function called the function execution context.
The function execution context is pushed on top of the global execution context.

```js
console.log(a);
var a = 10;
function test() {
  console.log(b);
  let b = 20;
}
test();
```

Output : 
```bash
undefined
12:11:16.010 VM374:1 Uncaught ReferenceError: Cannot access 'b' before initialization
    at test (<anonymous>:1:57)
    at <anonymous>:1:74
```

a. During creationphase a global execution context is created and pushed into the call stack
b. Memory is allocated for variable a and function test
c. Once the engine has scanned through the code, it starts executing the code and execution goes as below 
Line 1 : The value of variable a is printed which is undefined, because the memory is allocated during creation with variable assigned to an undefined value but the actual value is allocated during execution
Line 2 : The value of 10 is assigned to variable a 
Line 3-6 : function test is encountered but the definition is already stored during execution phase therefore nothing happens
Line 7 : The function test is called and a new functional execution context is created and pushed to the call stack with reference of Global execution context as outer environment and the creation phase starts for this functional execution context
Line 5 : Memory for variable b is allocated with no value and creation completes
Line 4 : The value is printed as ReferenceError because the memory was allocated during creation but the value is not assigned yet
Line 5 : The value of 20 is assigned to the variable 
Line 6 : The execution for functional context completes and is removed from the call stack
Line 7 : Once the execution completes, the global execution context is also removed from the call stack


Note : The key distinction for `var`, `let` and `const` is that value is initialised to `undefined` and stored in the `variable environment` for `var`.
However for `let` and `const`, the value is not initialized and kept in `Temporal Dead Zone` and they are stored in the `Lexical environment`.

```js
var b = 100;

function test() {
  console.log(b);
  var b = 20;
}

test();
```

Output 
```bash
undefined
```

Here the execution will go like below 
The memory is allocated to var b during Global Execution Context creation.
The value of 100 is assigned to b during the execution of global context.
During creation of the functional execution context, the global variable b is shadowed by the lexical scoped variable b and the output will be again undefined.


## Call Stack
Call stack is a mechanism for an interpreter to keep track of its place in the script, which function called within another function etc.
Javascript operates in a single threaded environment therefore it can execute only one operation at a time. The call stack is the part of Javascript that keeps track of the execution process.


