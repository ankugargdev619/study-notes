DOM : Document Object Model
The html inside the browser is converted into an object structure by the browser so that the browser can interact with it.

Node types in DOM
1. Element Node 
2. Text Node 
3. Comment Node
4. Document Node

## Selecting Elements
`querySelector` : Returns first match
```js
const btn = document.querySelector(".btn");
```

`querySelectorAll` : Returns the static NodeList
```js
const items = document.querySelectorAll(".item");
```
**Note** : If a new item is added to the item class then the list is not updated.

`getElementsByClassName` : Returns live HTMLCollection
```js 
const items = document.getElementsByClassName("item");
```

## DOM traversal
**Parent** : `el.parentElement`
Children : `el.children`
childNodes : `el.childNodes`

**Note** : The difference between children and childNodes is that the childNodes return the text nodes as well.

## Creating Elements
`createElement`
```js
const div = document.createElement("div");
```

`textContent`
```js
div.textContent = "Hello";
```

`innerHTML`
```js
div.innerHTML = "<b>Hello</b>";
```

XSS Edge Cases
```js
div.innerHTML = userInput;
```

If user enters
```js
<script>alert(1)</script>
```

`textContent` is preferable over `innerHTML`

## Appending Elements
`appendChild`
```js
parent.appeendChild(child);
```

Important Edge Case 
```js 
const el = document.createElement("div");

parent1.appendChild(el);
parent2.appendChild(el);
```

In this case, the element will be pushed to the first element only because here we are creating a new node as an element and the node can be present at one place at a time.

## Cloning Nodes
```js 
const clone = el.childNodes(true);
```
with `true` as an argument, the deep clone is created which means that all the child nodes are also copied.
If the argument is not passed then only the selected node is copied.

**Note** : Even if the copy is clone, the event listeners are not copied.

## Removing Elements 

