#include <bits/stdc++.h>
using namespace std;

class QueueNode {
    public:
        int data;
        QueueNode* next;
};

//Function to create a new node 
QueueNode* NewNode(int data) {
    QueueNode* queueNode = new QueueNode();
    queueNode->data = data;
    queueNode->next = NULL;
    return queueNode;
}

//Queue is empty or not
int isEmpty(QueueNode* root){
    return !root;
}

//enqueue an element to queue
void enqueue(QueueNode** root, int data){
    QueueNode* newNode = NewNode(data);
    if (isEmpty(*root)){
        *root = newNode;
        return;
    }

    QueueNode* temp = *root;
    while(temp->next != NULL){
        temp = temp->next;
    }
}

void dequeue(QueueNode** root){
    if (isEmpty(*root)){
        return INT_MIN;
    }
    QueueNode* temp = *root;
    int data = temp->data;
    *root = (*root)->next;
    delete temp;
    return data;
}
