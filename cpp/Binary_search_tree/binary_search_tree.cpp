#include <iostream>
using namespace std;

// Define a struct for the tree node
struct Node {
    int data;
    Node* left;
    Node* right;
};

// Function to create a new node in the tree
Node* createNode(int value) {
    Node* newNode = new Node();
    newNode->data = value;
    newNode->left = nullptr;
    newNode->right = nullptr;
    return newNode;
}

// Function to insert a node in the binary search tree
Node* insert(Node* root, int value) {
    if (root == nullptr) {
        return createNode(value); // If the root is empty, create a new node
    }
    if (value < root->data) {
        root->left = insert(root->left, value); // Recursively insert in the left subtree
    } else if (value > root->data) {
        root->right = insert(root->right, value); // Recursively insert in the right subtree
    }
    return root;
}

// Function to search for a value in the tree
bool search(Node* root, int value) {
    if (root == nullptr) {
        return false; // If the tree is empty, return false
    }
    if (root->data == value) {
        return true; // Value found
    } else if (value < root->data) {
        return search(root->left, value); // Search in the left subtree
    } else {
        return search(root->right, value); // Search in the right subtree
    }
}

// Function to find the leftmost node (smallest value)
int leftMostValue(Node* root) {
    while (root->left != nullptr) {
        root = root->left;
    }
    return root->data;
}

// Function to delete a node from the tree
Node* deleteNode(Node* root, int value) {
    if (root == nullptr) {
        return root;
    }
    if (value < root->data) {
        root->left = deleteNode(root->left, value);
    } else if (value > root->data) {
        root->right = deleteNode(root->right, value);
    } else {
        if (root->left == nullptr) {
            Node* temp = root->right;
            delete root;
            return temp;
        } else if (root->right == nullptr) {
            Node* temp = root->left;
            delete root;
            return temp;
        }
        root->data = leftMostValue(root->right);
        root->right = deleteNode(root->right, root->data);
    }
    return root;
}

// Function to perform pre-order traversal (root, left, right)
void preOrder(Node* root) {
    if (root != nullptr) {
        cout << root->data << " ";
        preOrder(root->left);
        preOrder(root->right);
    }
}

// Function to perform in-order traversal (left, root, right)
void inOrder(Node* root) {
    if (root != nullptr) {
        inOrder(root->left);
        cout << root->data << " ";
        inOrder(root->right);
    }
}

// Function to perform post-order traversal (left, right, root)
void postOrder(Node* root) {
    if (root != nullptr) {
        postOrder(root->left);
        postOrder(root->right);
        cout << root->data << " ";
    }
}

// Function to free the allocated memory for the tree
void freeTree(Node* root) {
    if (root == nullptr) {
        return;
    }
    freeTree(root->left);
    freeTree(root->right);
    delete root;
}

int main() {
    Node* root = nullptr;

    // Insert values into the tree
    root = insert(root, 25);
    root = insert(root, 15);
    root = insert(root, 50);
    root = insert(root, 10);
    root = insert(root, 22);
    root = insert(root, 35);
    root = insert(root, 70);
    root = insert(root, 4);
    root = insert(root, 12);
    root = insert(root, 18);
    root = insert(root, 24);
    root = insert(root, 31);
    root = insert(root, 44);
    root = insert(root, 66);
    root = insert(root, 90);

    // Pre-order traversal (VLR)
    cout << "Pre-order (VLR): ";
    preOrder(root);
    cout << endl;

    // In-order traversal (LVR)
    cout << "In-order (LVR): ";
    inOrder(root);
    cout << endl;

    // Post-order traversal (LRV)
    cout << "Post-order (LRV): ";
    postOrder(root);
    cout << endl;

    // Insert a duplicate element
    cout << "Insert element 15 into BST" << endl;
    insert(root, 15);
    cout << "In-order (LVR) after inserting 15: ";
    inOrder(root);
    cout << endl;

    // Remove an element
    cout << "Delete 50 from BST" << endl;
    root = deleteNode(root, 50);
    cout << "In-order (LVR) after deleting 50: ";
    inOrder(root);
    cout << endl;

    // Free the memory allocated for the tree
    freeTree(root);
    root = nullptr;

    return 0;
}
