#include <iostream>
using namespace std;

// Function to perform Bubble Sort
void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n-1; i++) {  // Loop for each pass
        for (int j = 0; j < n-i-1; j++) {  // Loop for comparing adjacent elements
            if (arr[j] > arr[j+1]) {
                // Swap if the element found is greater than the next element
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
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

    bubbleSort(arr, n);  // Call to Bubble Sort function

    cout << "Sorted array: ";
    printArray(arr, n);  // Print the sorted array

    return 0;
}
