#include <iostream>
using namespace std;

// Function to perform Insertion Sort
void insertionSort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i];  // The element to be inserted into the sorted portion
        int j = i - 1;

        // Move elements of arr[0..i-1], that are greater than the key, to one position ahead
        while (j >= 0 && arr[j] < key) {
            arr[j+1] = arr[j];
            j = j - 1;
        }

        // Insert the key into the correct position
        arr[j + 1] = key;
    }
}

// Function to print the array
void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;
}

int main() {
    int arr[] = {64, 34, 25, 12, 22, 11, 90};  // Example array
    int n = sizeof(arr) / sizeof(arr[0]);

    cout << "Unsorted array: ";
    printArray(arr, n);

    insertionSort(arr, n);  // Call to Insertion Sort function

    cout << "Sorted array: ";
    printArray(arr, n);  // Print the sorted array

    return 0;
}
