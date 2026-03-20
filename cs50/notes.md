# Linked List implementation
```c
#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct node {
  int number; // This will store the value
  struct node *next; //This will store memory address of the next item
}


int main(void) {
  node *list = NULL;  // Start with a memory allocation that points to NULL location in memory

  for(int i = 0; i < 3; i++) {
    node *n = malloc(sizeof(node)); // allocate memory for size equal to the node data structure (includes space for number to be stored and pointer to next node)

    if(n==NULL) {
      return 1; // Return if something goes wrong while allocating memory
    }

    n->number = get_int("Number: "); // Get input from user and store the value at the location the n is pointing to in number field of type struct we defined earlier
    n->next = NULL; // Point the next data pointer to NULL initially

    // Prepend to node list
    n->next = list // Point the next field in node type struct to where list is pointing i.e. NULL initially but later it will be pointing to the last node which was added to the list

      list = n; // Point the list to the new node which has been created
  }


  // Print the data
  node *ptr = list;
  while(ptr != NULL) {
    printf("%i\n",ptr->number);
    ptr = ptr->next;
  }
  
  return 0;
}

```
