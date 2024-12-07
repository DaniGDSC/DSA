#include <iostream>
using namespace std;

// Function to perform Selection Sort in decreasing order
void selectionSort(int arr[], int n) {
    for (int i = 0; i < n-1; i++) {
        // Find the maximum element in the remaining unsorted array
        int maxIndex = i;
        for (int j = i+1; j < n; j++) {
            if (arr[j] > arr[maxIndex]) {
                maxIndex = j;  // Update maxIndex if a larger element is found
            }
        }

        // Swap the maximum element with the first element of the unsorted part
        if (maxIndex != i) {
            int temp = arr[i];
            arr[i] = arr[maxIndex];
            arr[maxIndex] = temp;
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

    selectionSort(arr, n);  // Call to Selection Sort function

    cout << "Sorted array (Decreasing order): ";
    printArray(arr, n);  // Print the sorted array

    return 0;
}
