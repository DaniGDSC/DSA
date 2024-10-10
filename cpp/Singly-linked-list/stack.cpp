#include <bits/stdc++.h>
using namespace std;

class StackNode {
    public: 
        int data;
        StackNode* next;
};

// Function to create a new node
StackNode* newNode(int data) {
    StackNode* stackNode = new StackNode();
    stackNode->data = data;
    stackNode->next = NULL;
    return stackNode;
}

// Function to check if the stack is empty
int isEmpty(StackNode* root) {
    return !root;
}

// Function to push an element to the stack
void push(StackNode** root, int data) {
    StackNode* stackNode = newNode(data);
    stackNode->next = *root;
    *root = stackNode;
    cout << data << " pushed to stack\n";
}

// Function to pop an element from the stack
int pop(StackNode** root) {
    if (isEmpty(*root))
        return INT_MIN;
    StackNode* temp = *root;
    *root = (*root)->next;
    int popped = temp->data;
    delete temp;  // Free memory of popped node
    return popped;
}

// Function to peek the top element of the stack
int peek(StackNode* root) {
    return root->data;
}

// Function to calculate the sum of all elements in the stack
int sumTotal(StackNode* root) {
    int sum = 0;
    StackNode* temp = root;
    while (temp != NULL) {
        sum += temp->data;
        temp = temp->next;
    }
    return sum;
}

int main() {
    StackNode* root = NULL;

    // Pushing elements onto the stack
    push(&root, 10);
    push(&root, 20);
    push(&root, 30);

    // Peek the top element
    cout << "Top element is " << peek(root) << endl;

    // Calculate and display the sum of all elements in the stack
    cout << "Total sum of elements in stack: " << sumTotal(root) << endl;

    // Pop and display elements from the stack
    cout << "Elements present in stack: ";
    while (!isEmpty(root)) {
        cout << peek(root) << " ";
        pop(&root);
    }

    return 0;
}
