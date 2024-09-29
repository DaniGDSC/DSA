#include <stdio.h>
#include <stdlib.h> // Include this for malloc and free

// Define the structure for a node in the linked list
struct Node {
    int data;
    struct Node* next;
};

// Define the structure for the linked list, including a tail pointer
struct LinkedList {
    struct Node* head;
    struct Node* tail;
};

// Function to insert a new node at the end of the linked list
void insertAtEnd(struct LinkedList* list, int new_data) {
    // Allocate memory for the new node
    struct Node* new_node = (struct Node*)malloc(sizeof(struct Node));
    if (new_node == NULL) {
        printf("Memory allocation failed\n");
        return;
    }
    new_node->data = new_data;
    new_node->next = NULL;

    // If the list is empty, make the new node both head and tail
    if (list->head == NULL) {
        list->head = list->tail = new_node;
    } else {
        // Otherwise, add the new node to the end of the list
        list->tail->next = new_node;
        list->tail = new_node;
    }
}

// Function to insert a new node at the beginning of the linked list
void push(struct LinkedList* list, int new_data) {
    // Allocate memory for the new node
    struct Node* new_node = (struct Node*)malloc(sizeof(struct Node));
    if (new_node == NULL) {
        printf("Memory allocation failed\n");
        return;
    }
    new_node->data = new_data;
    new_node->next = list->head;

    // Update the head pointer to point to the new node
    list->head = new_node;

    // If the list was empty, also update the tail pointer
    if (list->tail == NULL) {
        list->tail = new_node;
    }
}

// Function to insert a new node after a given target value in the linked list
void insertAfterValue(struct LinkedList* list, int target_value, int new_data) {
    // Allocate memory for the new node
    struct Node* new_node = (struct Node*)malloc(sizeof(struct Node));
    if (new_node == NULL) {
        printf("Memory allocation failed\n");
        return;
    }
    new_node->data = new_data;
    new_node->next = NULL;

    // Traverse the list to find the target value
    struct Node* temp = list->head;
    while (temp != NULL && temp->data != target_value) {
        temp = temp->next;
    }

    // If the target value is not found, do nothing
    if (temp == NULL) {
        printf("Target value not found\n");
        free(new_node);
        return;
    }

    // Insert the new node after the target node
    new_node->next = temp->next;
    temp->next = new_node;

    // If the target node was the tail, update the tail pointer to point to the new node
    if (temp == list->tail) {
        list->tail = new_node;
    }
}

// Function to print the linked list
void printList(struct LinkedList* list) {
    struct Node* temp = list->head;
    while (temp != NULL) {
        printf("%d ", temp->data);
        temp = temp->next;
    }
    printf("\n");
}

int main() {
    // Initialize the linked list, including a tail pointer
    struct LinkedList list;
    list.head = list.tail = NULL;

    int n, value;
    printf("Enter number of elements: ");
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        printf("Enter element %d: ", i + 1);
        scanf("%d", &value);
        insertAtEnd(&list, value); // Use the correct function to add elements
    }

    int target_value, new_data;
    printf("Enter target value after which to insert: ");
    scanf("%d", &target_value);
    printf("Enter new data to insert: ");
    scanf("%d", &new_data);

    insertAfterValue(&list, target_value, new_data); // Insert the new element

    printf("Linked list elements are: ");
    printList(&list); // Print the linked list
    return 0;
}
