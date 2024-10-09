#include <iostream>
#include <stdexcept>
using namespace std;

// Queue class implementation using a singly linked list
class Queue {
private:
    // Node structure for the linked list
    struct Node {
        int data;
        Node* next;
        Node(int value) : data(value), next(nullptr) {}
    };
    
    Node* front_;  // Pointer to the front of the queue
    Node* rear_;   // Pointer to the rear of the queue
    int size_;     // Number of elements in the queue

public:
    // Constructor: Initialize an empty queue
    Queue() : front_(nullptr), rear_(nullptr), size_(0) {}
    
    // Destructor: Clean up the queue
    ~Queue() {
        clear();
    }
    
    // Add an element to the rear of the queue
    void enqueue(int value) {
        Node* newNode = new Node(value);
        if (isEmpty()) {
            front_ = rear_ = newNode;
        } else {
            rear_->next = newNode;
            rear_ = newNode;
        }
        size_++;
    }
    
    // Remove and return the front element of the queue
    int dequeue() {
        if (isEmpty()) {
            throw  runtime_error("Queue is empty");
        }
        int value = front_->data;
        Node* temp = front_;
        front_ = front_->next;
        delete temp;
        size_--;
        if (isEmpty()) {
            rear_ = nullptr;
        }
        return value;
    }
    
    // Remove all elements from the queue
    void clear() {
        while (!isEmpty()) {
            dequeue();
        }
    }
    
    // Check if the queue is empty
    bool isEmpty() const {
        return size_ == 0;
    }
    
    // Return the front element without removing it
    int front() const {
        if (isEmpty()) {
            throw  runtime_error("Queue is empty");
        }
        return front_->data;
    }
    
    // Return the number of elements in the queue
    int size() const {
        return size_;
    }
    
    // Print the contents of the queue
    void print() const {
        if (isEmpty()) {
            cout << "Queue is empty" <<  endl;
            return;
        }
        
        Node* current = front_;
         cout << "Queue: ";
        while (current != nullptr) {
            cout << current->data;
            if (current->next != nullptr) {
                 cout << " -> ";
            }
            current = current->next;
        }
        cout << endl;
    }
};

// Example usage of the Queue class
int main() {
    Queue q;
    
    // Enqueue some elements
    q.enqueue(1);
    q.enqueue(2);
    q.enqueue(3);
    
    // Print initial state
    cout << "Initial state:" <<  endl;
    q.print();
    
    // Demonstrate front() and dequeue() operations
    cout << "Front element: " << q.front() <<  endl;
    cout << "Dequeued: " << q.dequeue() <<  endl;
    
    // Print state after dequeue
    cout << "After dequeue:" << endl;
    q.print();
    
    // Enqueue another element
    q.enqueue(4);
     cout << "After enqueueing 4:" <<  endl;
    q.print();
    
    // Clear the queue and print the result
    q.clear();
     cout << "After clear:" <<  endl;
    q.print();
    
    return 0;
}