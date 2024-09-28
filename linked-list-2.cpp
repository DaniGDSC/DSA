#include <iostream>
using namespace std;

// Define the structure for a node in the linked list
struct Node {
    int data;
    struct Node* next;
};

// Function to insert a new element after one element which contains given value in linked list
void insertAfterValue(struct Node** head_ref, int target_value, int new_data) {
    // Allocate memory for the new node
    struct Node* new_node = (struct Node*)malloc(sizeof(struct Node));
    if (new_node == NULL) {
        cout << "Memory allocation failed" << endl;
        return;
    }
    new_node->data = new_data;
    new_node->next = NULL;

    // If the list is empty, make the new node as head
    if (*head_ref == NULL) {
        *head_ref = new_node;
        return;
    }

    struct Node* temp = *head_ref; // Traverse to find the target value
    while (temp != NULL && temp->data != target_value) {
        temp = temp->next;
    }

    // If the target value is not found, do nothing
    if (temp == NULL) {
        cout << "Target value not found in the list" << endl;
        free(new_node); // Free the allocated memory for the new node
        return;
    }

    // Insert the new node after the found node
    new_node->next = temp->next;
    temp->next = new_node;

    cout << "New element inserted successfully" << endl;
}

// Function to add a new element at the end of the linked list
void insertAtEnd(struct Node** head_ref, int new_data) {
    // Allocate memory for the new node
    struct Node* new_node = (struct Node*)malloc(sizeof(struct Node));
    new_node->data = new_data;
    new_node->next = NULL; // The new node should point to NULL initially

    if (*head_ref == NULL) { // If the list is empty, make the new node as head
        *head_ref = new_node;
        return;
    }

    struct Node* temp = *head_ref; // Traverse to the end of the list
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = new_node; // Add the new node at the end
}

// Function to print the linked list
void printList(struct Node* head) {
    struct Node* temp = head;
    while (temp != NULL) {
        cout << temp->data << " -> ";
        temp = temp->next;
    }
    cout << "NULL" << endl;
}

int main() {
    // Create a linked list: 1 -> 2 -> 3
    struct Node* head = NULL;
    insertAtEnd(&head, 1);
    insertAtEnd(&head, 2);
    insertAtEnd(&head, 3);

    cout << "Original List: ";
    printList(head);

    // Insert a new element after the node with value 2
    insertAfterValue(&head, 1, 5);

    cout << "Updated List: ";
    printList(head);

    return 0;
}
