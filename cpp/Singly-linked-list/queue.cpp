#include <iostream>
#include <stdexcept>
using namespace std;

class Queue {
private:
    struct Node {
        int data;
        Node* next;
        Node(int value) : data(value), next(nullptr) {}
    };
    
    Node* front_;
    Node* rear_;
    int size_;

public:
    Queue() : front_(nullptr), rear_(nullptr), size_(0) {}
    
    ~Queue() {
        Node* current = front_;
        while (current != nullptr) {
            Node* temp = current;
            current = current->next;
            delete temp;
        }
    }
    
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
    
    int dequeue() {
        if (isEmpty()) {
            throw runtime_error("Queue is empty");
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
    
    void clear() {
        Node* current = front_;
        while (current != nullptr) {
            Node* temp = current;
            current = current->next;
            delete temp;
        }
        front_ = rear_ = nullptr;
        size_ = 0;
    }
    
    bool isEmpty() const {
        return size_ == 0;
    }
    
    int front() const {
        if (isEmpty()) {
            throw runtime_error("Queue is empty");
        }
        return front_->data;
    }

    int secondElement() const {
        if (isEmpty()) {
            throw runtime_error("Queue is empty");
        }
        if (front_->next == nullptr) {
            throw runtime_error("Queue has only one element");
        }
        return front_->next->data;
    }
    
    int size() const {
        return size_;
    }

    bool search(int value) const {
        Node* current = front_;
        while (current != nullptr) {
            if (current->data == value) {
                return true;
            }
            current = current->next;
        }
        return false;
    }
    
    void print() const {
        if (isEmpty()) {
            cout << "Queue is empty" << endl;
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

    int sumNegativeValues() const {
        int sum = 0;
        Node* current = front_;
        while (current != nullptr) {
            if (current->data < 0) {
                sum += current->data;
            }
            current = current->next;
        }
        return sum;
    }
};

int main() {
    Queue q;
    
    // Enqueue some elements
    q.enqueue(1);
    q.enqueue(-2);
    q.enqueue(3);
    q.enqueue(-4);
    
    cout << "Initial state:" << endl;
    q.print();
    
    cout << "Front element: " << q.front() << endl;
    cout << "Second element: " << q.secondElement() << endl;
    cout << "Dequeued: " << q.dequeue() << endl;
    
    cout << "After dequeue:" << endl;
    q.print();
    
    q.enqueue(5);
    cout << "After enqueueing 5:" << endl;
    q.print();

    cout << "3 exists in the queue: " << (q.search(3) ? "yes" : "no") << endl;
    cout << "6 exists in the queue: " << (q.search(6) ? "yes" : "no") << endl;

    cout << "Sum of negative values: " << q.sumNegativeValues() << endl;
    
    q.clear();
    cout << "After clear:" << endl;
    q.print();
    
    return 0;
}